from flask import g

from flask_apm.collector.request_context import RequestContext


def with_request_context(func):
    def wrapper(*args, **kwargs):
        try:
            if 'apm_request_context' not in g:
                g.apm_request_context = RequestContext()
            func(g.apm_request_context, *args, **kwargs)
        except RuntimeError:
            pass
    return wrapper


def with_request_context_class(func):
    def wrapper(primary, *args, **kwargs):
        try:
            if 'apm_request_context' not in g:
                g.apm_request_context = RequestContext()
            func(primary, g.apm_request_context, *args, **kwargs)
        except RuntimeError:
            pass
    return wrapper
