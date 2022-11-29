
from logging import StreamHandler

from flask_apm.collector.utils import with_request_context_class


class ApmLoggingHandler(StreamHandler):

    def __init__(self):
        StreamHandler.__init__(self)

    @with_request_context_class
    def emit(self, request_context, record):
        msg = self.format(record)
        request_context.record_logging(record, msg)
