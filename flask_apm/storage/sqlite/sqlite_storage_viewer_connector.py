from flask_apm.storage import ApmStorageViewerConnector
from flask_apm.storage.sqlite import db_access
from flask_apm.storage.sqlite.sqlite_storage_connector_base import SqliteStorageConnector
from flask_apm.storage.record import Record


class SqliteStorageViewerConnector(ApmStorageViewerConnector, SqliteStorageConnector):
    pass
    # def write_record(self, record: Record):
    #    db_access.RecordDbAccess.insert(self._conn, record)

