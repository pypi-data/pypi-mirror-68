import importlib
import json
import logging
import re
from http import HTTPStatus
from urllib.parse import urlencode

import json_log_formatter
from boltons.iterutils import remap
from ddtrace import tracer
from flask import g, jsonify, request
from flask_limiter import Limiter
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException, InternalServerError
from werkzeug.middleware.proxy_fix import ProxyFix

from .auth import get_user, role_required
from .platform_connection import PlatformConnectionError

SENSITIVE_KEYS = re.compile(r'password|token|secret|key', flags=re.I)
MAX_BODY_SIZE = 50000


def scrub_keys(path, key, value):
    if isinstance(key, str) and SENSITIVE_KEYS.search(key):
        return key, '-' * 5
    return key, value


def generate_json_handler():
    json_handler = logging.StreamHandler()
    json_handler.setFormatter(json_log_formatter.JSONFormatter())
    return json_handler


class DHPotluck:
    def __init__(self, app=None, **kwargs):
        """Initialize dh-potluck."""
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        app_token = app.config['DH_POTLUCK_APP_TOKEN']
        validate_func_name = app.config.get('DH_POTLUCK_VALIDATE_TOKEN_FUNC',
                                            'dh_potluck.auth.validate_token_using_api')
        module_name, class_name = validate_func_name.rsplit('.', 1)
        validate_token_func = getattr(importlib.import_module(module_name), class_name)

        # Adjust the WSGI environ based on X-Forwarded- headers that proxies in front of the
        # application may set.
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

        # Disable tracing when testing
        tracer.configure(enabled=not app.config.get('TESTING', False))

        enable_rate_limiting = bool(app.config.get('RATELIMIT_ENABLED', 0))
        rate_limit = app.config.get('RATELIMIT_DEFAULT_PER_MINUTE', 1000)

        def key_func():
            if 'Authorization' in request.headers:
                return request.headers['Authorization'].split(' ')[1]
            else:
                ip = request.remote_addr
                if request.headers.getlist('X-Forwarded-For'):
                    ip = request.headers.getlist('X-Forwarded-For')[0]
                return ip

        self.limiter = Limiter(
            key_func=key_func,
            default_limits=[f'{rate_limit} per minute'],
            default_limits_per_method=False,
            headers_enabled=True,
            swallow_errors=True,
            enabled=enable_rate_limiting,
        )

        @self.limiter.request_filter
        def app_token_whitelist():
            return request.headers.get('Authorization', '') == f'Application {app_token}'

        self.limiter.init_app(app)

        @app.before_request
        def before_request():
            # Allow all OPTIONS requests so CORS works properly
            if request.method == 'OPTIONS':
                return
            return get_user(app_token, validate_token_func)

        # Catch webargs validation errors and return them in JSON format
        @app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
        def handle_unprocessable_entity(error):
            response = {
                'description': 'Input failed validation.',
                'errors': error.exc.messages,
            }
            return jsonify(response), HTTPStatus.BAD_REQUEST

        # Catch marshmallow validation errors and return them in JSON format
        @app.errorhandler(ValidationError)
        def handle_validation_error(error):
            response = {
                'description': 'Input failed validation.',
                'errors': error.messages,
            }
            return jsonify(response), HTTPStatus.BAD_REQUEST

        # Catch SQLAlchemy IntegrityErrors (usually unique constraint violations) and return them
        # in JSON format. TODO: Right now we return the database error as-is to the client. This
        # should be expanded to parse the integrity error and try to build a more structured,
        # user-friendly message about the error.
        @app.errorhandler(IntegrityError)
        def handle_integrity_errors(error):
            return (jsonify({'description': f'Database integrity error: {error.orig.args[1]}'}),
                    HTTPStatus.BAD_REQUEST)

        # Ensure all other Flask HTTP exceptions are returned in JSON format
        @app.errorhandler(HTTPException)
        def handle_flask_exceptions(error):
            return jsonify({'description': error.description}), error.code

        # Add extra context to Datadog traces for server errors
        @app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
        def handle_server_error(error):
            error_response = (
                jsonify({'description': InternalServerError.description}),
                HTTPStatus.INTERNAL_SERVER_ERROR
            )

            span = tracer.current_root_span()
            if span:
                # Log query string (if present) for all request methods
                query_params = request.args
                if query_params:
                    clean = remap(query_params.copy(), visit=scrub_keys)
                    span.set_tag('http.query_string', urlencode(clean))

                # Skip body logging if not POST, PATCH or PUT
                if request.method not in ['POST', 'PATCH', 'PUT']:
                    return error_response

                # Skip body logging if it's empty
                if not request.content_length:
                    return error_response

                span.set_tag('http.content_length', request.content_length)

                if request.content_length > MAX_BODY_SIZE:
                    span.set_tag('http.body', 'Body too large, content could not be logged.')
                    return error_response

                # Try to parse body as JSON, and scrub sensitive values
                body = request.get_json(silent=True)
                if body:
                    clean = remap(body, visit=scrub_keys)
                    span.set_tag('http.body', json.dumps(clean))
                else:
                    # If we can't parse as JSON, log the raw body
                    body = request.get_data(as_text=True)
                    span.set_tag('http.body', body)

            return error_response

        @app.errorhandler(HTTPStatus.TOO_MANY_REQUESTS)
        def handle_too_many_requests(error):
            error_response = (
                jsonify({'description': 'Too Many Requests!'}),
                HTTPStatus.TOO_MANY_REQUESTS
            )

            if 'Authorization' in request.headers:
                key = key_func()
                cleaned_key = f'{key[0:4]}...{key[-4:-1]}'
            else:
                cleaned_key = request.remote_addr

            tracer.set_tags({'rate_limit_key': cleaned_key})

            return error_response

        @app.errorhandler(PlatformConnectionError)
        def handle_platform_connection_error(err):
            return jsonify({'description': str(err)}), HTTPStatus.BAD_REQUEST

        # Structured logging configuration
        if app.config.get('STRUCTURED_LOGGING'):

            # Set root logger handler
            root_logger = logging.getLogger()
            root_logger.handlers = [generate_json_handler()]

            # Set all others
            for logger in [logging.getLogger(name) for name in logging.root.manager.loggerDict]:
                logger.handlers = [generate_json_handler()]
                # Don't propagate back to root logger
                logger.propagate = False

            # Catch and log unhandled exceptions in json format
            @app.errorhandler(Exception)
            def handle_error(e):
                app.logger.error(e, exc_info=True)

    @staticmethod
    def role_required(*args, **kwargs):
        return role_required(*args, **kwargs)

    @property
    def current_user(self):
        return g.user
