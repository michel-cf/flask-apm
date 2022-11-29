from flask import template_rendered, before_render_template, got_request_exception, message_flashed

from flask_apm.collector.utils import with_request_context


@with_request_context
def log_template_rendered(request_context, sender, template, context, **extra):
    request_context.log_template_rendered(template, context)


@with_request_context
def log_before_template_render(request_context, sender, template, context, **extra):
    request_context.log_before_template_render(template, context)


def log_request(sender, **extra):
    sender.logger.debug('Request context is set up')


def log_response(sender, response, **extra):
    sender.logger.debug('Request context is about to close down. '
                        'Response: %s', response)


@with_request_context
def log_exception(request_context, sender, exception, **extra):
    request_context.log_exception(exception)
    sender.logger.debug('Exception during request handling. '
                        'Exception: %s', exception)


@with_request_context
def record_message_flashed(request_context, sender, message, category, **extra):
    request_context.record_message_flashed(category, message)
    sender.logger.debug('Message flashed. '
                        'Category: %s, message: %s', category, message)


def connect_base_signal_listeners(app):
    got_request_exception.connect(log_exception, app)


def connect_template_signal_listeners(app):
    template_rendered.connect(log_template_rendered, app)
    before_render_template.connect(log_before_template_render, app)


def connect_message_flash_signal_listener(app):
    message_flashed.connect(record_message_flashed, app)
