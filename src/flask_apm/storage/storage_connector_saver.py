import abc

from flask_apm.storage.record import Record
from flask_apm.storage.storage_connector_base import ApmStorageConnectorBase


class ApmStorageSaverConnector(ApmStorageConnectorBase):

    @abc.abstractmethod
    def write_record(self, record: Record):
        pass
