from flask_apm.storage import ApmStorageViewerConnector
from flask_apm.storage.sqlite.sqlite_storage_connector_base import SqliteStorageConnector


class SqliteStorageViewerConnector(SqliteStorageConnector, ApmStorageViewerConnector):
    pass
    # def write_record(self, record: Record):
    #    db_access.RecordDbAccess.insert(self._conn, record)

