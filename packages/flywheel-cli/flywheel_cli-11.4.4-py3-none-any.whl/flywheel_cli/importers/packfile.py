"""Provides functions for creating packfiles"""
import logging

import fs
import fs.copy
import fs.path
from fs.zipfs import ZipFS

log = logging.getLogger(__name__)


class PackfileDescriptor:
    # pylint: disable=too-few-public-methods
    """PackfileDescriptor class"""
    def __init__(self, packfile_type, path, count, name=None):
        """Descriptor object for creating a packfile"""
        self.packfile_type = packfile_type
        self.path = path
        self.count = count
        self.name = name

def create_zip_packfile(dst_file, walker, packfile_type, compression=None, **kwargs):
    """Create a zipped packfile for the given packfile_type and options, that writes a ZipFile to dst_file

    Arguments:
        dst_file (file): The destination path or file object
        walker (AbstractWalker): The source walker instance
        packfile_type (str): The packfile type, or None
        subdir (str): The optional packfile subdirectory
        paths (list(str)): The list of paths to add to the packfile
        progress_callback (function): Function to call with byte totals
        deid_profile: The de-identification profile to use
    """
    if compression is None:
        import zipfile  # pylint: disable=import-outside-toplevel
        compression = zipfile.ZIP_DEFLATED

    with ZipFS(dst_file, write=True, compression=compression) as dst_fs:
        zip_member_count = create_packfile(walker, dst_fs, packfile_type, **kwargs)

    return zip_member_count

def create_packfile(walker, dst_fs, packfile_type, subdir=None, paths=None,
                    progress_callback=None, deid_profile=None, flatten=False):
    """Create a packfile by copying files from walker to dst_fs, possibly validating and/or de-identifying

    Arguments:
        walker (AbstractWalker): The source walker instance
        write_fn (function): Write function that takes path and bytes to write
        progress_callback (function): Function to call with byte totals
        deid_profile: The de-identification profile to use
    """
    progress = {'total_bytes': 0}

    # Report progress as total_bytes
    if callable(progress_callback):
        def progress_fn(dst_fs, path):
            progress['total_bytes'] += dst_fs.getsize(path)
            progress_callback(progress['total_bytes'])
    else:
        progress_fn = None

    if not paths:
        # Determine file paths
        paths = []
        for root, _, files in walker.walk(subdir=subdir):
            for file_info in files:
                paths.append(walker.combine(root, file_info.name))
    # Attempt to de-identify using deid_profile first
    if deid_profile.name != 'none':
        if deid_profile.process_packfile(packfile_type, walker, dst_fs, paths, callback=progress_fn):
            return len(paths) # Handled by de-id

    # Otherwise, just copy files into place
    for path in paths:
        # Ensure folder exists
        target_path = path
        if subdir:
            target_path = walker.remove_prefix(subdir, path)
        if flatten:
            target_path = fs.path.basename(path)
        folder = fs.path.dirname(target_path)
        dst_fs.makedirs(folder, recreate=True)
        with walker.open(path, 'rb') as src_file:
            dst_fs.upload(target_path, src_file)
        if callable(progress_fn):
            progress_fn(dst_fs, target_path)
    return len(paths)
