import atexit

from flask.app import Flask

from flask_apm.storage import ApmStorageViewerConnector
from flask_apm.storage.sqlite import SqliteStorageViewerConnector


class ApmUserInterface:
    __app = None
    __config = {}
    __storage_connector: ApmStorageViewerConnector

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.__app = app
        self.__config = app.config.get('APM', {})

        self.__storage_connector = SqliteStorageViewerConnector()
        self.__storage_connector.init(self.__config)

        atexit.register(self._app_teardown)

        # TODO register ui blueprint
        pass

    def _app_teardown(self):
        self.__storage_connector.close()
