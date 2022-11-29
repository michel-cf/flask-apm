import datetime
import json
import time

from flask import request
from werkzeug.datastructures import Headers

from flask_apm.storage import Record


class RequestContext:
    trace = []
    response_headers = None
    status_code = None
    has_exception = False

    def __init__(self):
        self.request_timestamp = time.time_ns()
        self.request_start = time.perf_counter_ns()
        self.request_start_process = time.process_time_ns()

    def record_logging(self, record, msg):
        self.trace.append({
            'type': 'logging',
            'timestamp': datetime.datetime.now().timestamp(),
            'level': record.levelname,
            'module': record.module,
            'filename': record.filename,
            'msg': msg,
        })

    def log_template_rendered(self, template, context):
        self.trace.append({
            'type': 'template_rendered',
            'timestamp': datetime.datetime.now().timestamp(),
            'template': template.name or 'string template'
        })

    def log_before_template_render(self, template, context):
        self.trace.append({
            'type': 'before_template_render',
            'timestamp': datetime.datetime.now().timestamp(),
            'template': template.name or 'string template'
        })

    def log_exception(self, exception):
        self.has_exception = True
        self.trace.append({
            'type': 'exception',
            'timestamp': datetime.datetime.now().timestamp(),
            'exception': exception
        })

    def record_message_flashed(self, category, message):
        self.trace.append({
            'type': 'message_flashed',
            'timestamp': datetime.datetime.now().timestamp(),
            'category': category,
            'message': message
        })

    def print(self):
        print(json.dumps({
            'request': {
                'method': request.method,
                'url': request.url,
                'query_string': str(request.query_string),
                'headers': _map_headers(request.headers),
                'path': request.path,
                'remote_addr': request.remote_addr
            },
            'response': {
                'status_code': self.status_code,
                'headers': _map_headers(self.response_headers),
            },
            'trace': self.trace,
        }))

    def as_record(self, trace_threshold_ms=200):
        response_time_ns = time.perf_counter_ns() - self.request_start
        response_process_time_ns = time.process_time_ns() - self.request_start_process

        record = Record()
        record.timestamp = self.request_timestamp
        record.response_time_ns = response_time_ns
        record.has_exception = self.has_exception

        record.request_method = request.method
        record.url = request.url
        record.status_code = self.status_code

        if self.has_exception or response_time_ns > (trace_threshold_ms * 1000000):
            record.response_process_time_ns = response_process_time_ns

            record.query_string = str(request.query_string)
            record.request_headers = json.dumps(_map_headers(request.headers))
            record.path = request.path
            record.remote_addr = request.remote_addr

            record.response_headers = json.dumps(_map_headers(self.response_headers))
            record.trace = json.dumps(self.trace)

        return record


def _map_headers(headers: Headers):
    header_dict = {}
    for key, value in headers.items():
        header_dict[key] = value
    return header_dict
