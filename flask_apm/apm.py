from flask.app import Flask

from flask_apm.apm_user_interface import ApmUserInterface
from flask_apm.apm_collector import ApmCollector


class Apm:
    collector: ApmCollector
    user_interface: ApmUserInterface

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask, collect_data: bool = True, serve_user_interface: bool = True):
        if collect_data:
            self.collector = ApmCollector(app)
        if serve_user_interface:
            self.user_interface = ApmUserInterface(app)

