import atexit
import logging

from flask import g
from flask.app import Flask

from flask_apm.collector import signal_listeners
from flask_apm.collector.logging_handler import ApmLoggingHandler
from flask_apm.collector.request_context import RequestContext
from flask_apm.storage import ApmStorageSaverConnector
from flask_apm.storage.sqlite import SqliteStorageSaverConnector


class ApmCollector:
    __app = None
    __config = {}
    __logging_initialized = False
    __logging_handler = ApmLoggingHandler()
    __storage_connector: ApmStorageSaverConnector

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.__app = app
        self.__config = app.config.get('APM', {})

        self.__storage_connector = SqliteStorageSaverConnector()
        self.__storage_connector.init(self.__config)

        atexit.register(self._app_teardown)

        app.before_request(self._before_request)
        app.after_request(self._after_request)

        signal_listeners.connect_base_signal_listeners(app)

        trace_config = self._get_trace_config()
        if trace_config.get('template', True):
            signal_listeners.connect_template_signal_listeners(app)

        if trace_config.get('flash_message', True):
            signal_listeners.connect_message_flash_signal_listener(app)

    # noinspection PyMethodMayBeStatic
    def _persist_request_context(self, apm_request_context: RequestContext, response):
        apm_request_context.response_headers = response.headers
        apm_request_context.status_code = response.status_code

        self.__storage_connector.write_record(apm_request_context.as_record())

    def _before_request(self):
        if not self.__logging_initialized:
            if self._get_trace_config().get('logging', True):
                logger = logging.getLogger()
                self.__logging_handler.setLevel('DEBUG')
                logger.addHandler(self.__logging_handler)
            self.__logging_initialized = True

        if 'apm_request_context' not in g:
            g.apm_request_context = RequestContext()

    def _after_request(self, response):
        if 'apm_request_context' in g:
            self._persist_request_context(g.apm_request_context, response)
            del g.apm_request_context
        return response

    def _get_trace_config(self):
        return self.__config.get('trace', {})

    def _app_teardown(self):
        self.__storage_connector.close()
