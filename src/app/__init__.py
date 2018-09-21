import logging

from flask import Blueprint, Flask
from flask_restful import Api
from applicationinsights.flask.ext import AppInsights

from app.config import Config
from app.opcua_connector import OpcUaConnector
from app.monitoring_service import MonitoringService

api_bp = Blueprint('api', __name__)
appinsights = AppInsights()
connector = OpcUaConnector()
monitor = MonitoringService()
api = Api(api_bp)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # register api blueprint
    url_prefix = '/api/{api_version}'.format(api_version=app.config['API_VERSION'])
    app.register_blueprint(api_bp, url_prefix=url_prefix)

    with app.app_context():
        connector.init_app(app)
        appinsights.init_app(app)
        monitor.init_app(app)

        # register application logging interface
        log_level = app.config['LOG_LEVEL'].upper()
        log_level = logging.DEBUG if log_level == 'TRACE' else log_level
        app.logger.setLevel(log_level)

    return app

from app import routes
