import sqlite3
from sqlite3 import Error

from flask_apm.storage.sqlite import db_access


class SqliteStorageConnector:
    _conn = None

    def init(self, conf):
        # TODO make db configurable
        if self.create_connection('apm.db'):
            sqlite3.register_adapter(bool, int)
            sqlite3.register_converter("BOOLEAN", lambda v: v != '0')

            self._migrate()

    def close(self):
        if self._conn is not None:
            self._conn.close()

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        try:
            self._conn = sqlite3.connect(db_file, check_same_thread=False)
            return True
        except Error as e:
            print(e)
            return False

    def _migrate(self):
        for db_accessor in db_access.DB_ACCESSORS:
            db_accessor.migrate(self._conn)

