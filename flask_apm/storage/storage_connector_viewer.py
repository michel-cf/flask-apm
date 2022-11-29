import abc

from flask_apm.storage.record import Record
from flask_apm.storage.storage_connector_base import ApmStorageConnectorBase


class ApmStorageViewerConnector(ApmStorageConnectorBase):
    pass

    # @abc.abstractmethod
    # def write_record(self, record: Record):
    #    pass
