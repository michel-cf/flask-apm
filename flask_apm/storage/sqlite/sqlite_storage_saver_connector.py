from flask_apm.storage import ApmStorageSaverConnector
from flask_apm.storage.sqlite import db_access
from flask_apm.storage.sqlite.sqlite_storage_connector_base import SqliteStorageConnector
from flask_apm.storage.record import Record


class SqliteStorageSaverConnector(ApmStorageSaverConnector, SqliteStorageConnector):

    def write_record(self, record: Record):
        db_access.RecordDbAccess.insert(self._conn, record)

