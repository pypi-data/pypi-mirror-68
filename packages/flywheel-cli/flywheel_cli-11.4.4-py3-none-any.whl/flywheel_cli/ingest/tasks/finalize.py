"""Provides FinalizeTask class"""

import logging
import os
import tempfile

from ... import util
from .. import models as M
from .. import schemas as T
from .abstract import Task

log = logging.getLogger(__name__)


class FinalizeTask(Task):
    """Finalize ingest. Currently uploading audit log to target projects."""

    def _run(self):
        """Upload audit log to every project that we identified
        TODO: group logs by project
        """
        if self.ingest_config.no_audit_log:
            log.debug("Audit log turned off, so skip uploading it")
            return
        with tempfile.TemporaryDirectory() as tmp_dir:
            filepath = util.get_filepath(tmp_dir, prefix="audit_log")
            filename = os.path.basename(filepath)
            with open(filepath, "w") as fp:
                for log_line in self.db.audit_logs:
                    fp.write(log_line)
            with open(filepath, "rb") as fp:
                project_containers = self.db.get_all_container(
                    M.Container.level == T.ContainerLevel.project
                )
                for container in project_containers:
                    self.fw.upload(
                        container.level.name,
                        container.dst_context.get("_id"),
                        filename,
                        fp,
                    )

    def _on_success(self):
        self.db.set_ingest_status(T.IngestStatus.finished)

    def _on_error(self):
        self.db.fail()
