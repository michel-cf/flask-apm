import abc
import sqlite3
from typing import Union, Any, Optional, Tuple

from flask_apm.storage import Record


class DbAccess(abc.ABC):
    _table_name = None
    _model = None
    _mapping = None

    @classmethod
    @abc.abstractmethod
    def migrate(cls, conn: sqlite3.Connection):
        pass

    @classmethod
    def _table_exists(cls, db: Union[sqlite3.Connection, sqlite3.Cursor]) -> bool:
        cursor = db.cursor()
        cursor.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=?;', (cls._table_name,))
        table_exists = cursor.fetchone() is not None
        cursor.close()
        return table_exists

    @classmethod
    def _get_column_info(cls, conn: sqlite3.Connection, column_name: str) -> Optional[Tuple[str, bool, Any, bool]]:
        cursor = conn.cursor()
        cursor.execute('PRAGMA table_info(\'' + cls._table_name + '\')')
        for column_info in cursor:
            if column_info[1] == column_name:
                return column_info[2], bool(column_info[3]), column_info[4], bool(column_info[5])
        return None

    @classmethod
    def _has_column(cls, conn: sqlite3.Connection, column_name: str) -> bool:
        return cls._get_column_info(conn, column_name) is not None

    @classmethod
    def _get_column_type(cls, conn: sqlite3.Connection, column_name: str) -> Optional[str]:
        column_info = cls._get_column_info(conn, column_name)
        if column_info is not None:
            return column_info[0]
        return None

    @classmethod
    def _is_column_not_null(cls, conn: sqlite3.Connection, column_name: str) -> Optional[bool]:
        column_info = cls._get_column_info(conn, column_name)
        if column_info is not None:
            return column_info[1]
        return None

    @classmethod
    def _get_column_default_value(cls, conn: sqlite3.Connection, column_name: str) -> Optional[Any]:
        column_info = cls._get_column_info(conn, column_name)
        if column_info is not None:
            return column_info[2]
        return None

    @classmethod
    def _is_column_pk(cls, conn: sqlite3.Connection, column_name: str) -> Optional[bool]:
        column_info = cls._get_column_info(conn, column_name)
        if column_info is not None:
            return column_info[3]
        return None

    @classmethod
    def insert(cls, conn: sqlite3.Connection, model_instance):
        if isinstance(model_instance, cls._model):
            query = 'insert into ' + cls._table_name + '('
            query_value_string = ''
            values = []
            for model_field_name, model_value in model_instance.__dict__.items():
                if not callable(model_value) and not model_field_name.startswith('__'):
                    if len(query_value_string) > 0:
                        query += ', '
                        query_value_string += ', '
                    query += model_field_name
                    query_value_string += '?'
                    values.append(model_value)
            if len(values) > 0:
                query += ') values (' + query_value_string + ');'
                conn.execute(query, values)
                conn.commit()


class RecordDbAccess(DbAccess):
    _table_name = 'record'
    _model = Record

    @classmethod
    def migrate(cls, conn: Union[sqlite3.Connection, sqlite3.Cursor]):
        if not cls._table_exists(conn):
            conn.execute('''CREATE TABLE record(
                                ID                          INTEGER PRIMARY KEY AUTOINCREMENT,
                                timestamp                   INT             NOT NULL,
                                
                                response_time_ns            INT             NOT NULL,
                                response_process_time_ns    INT             NULL,
                                
                                has_exception               BOOLEAN         NOT NULL,
                                
                                request_method              CHAR(40)        NOT NULL,
                                url                         TEXT            NOT NULL,
                                query_string                TEXT            NULL,
                                request_headers             TEXT            NULL,
                                path                        TEXT            NULL,
                                remote_addr                 TEXT            NULL,
                                
                                status_code                 CHAR(10)        NOT NULL,
                                response_headers            TEXT            NULL,
                                trace                       TEXT            NULL);'''
                         )
        #print(cls._is_column_pk(conn, 'ID'))


DB_ACCESSORS = (RecordDbAccess,)
