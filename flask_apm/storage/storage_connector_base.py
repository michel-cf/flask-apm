import abc


class ApmStorageConnectorBase(abc.ABC):

    def init(self, conf: dict):
        pass

    def close(self):
        pass
