from applicationinsights import TelemetryClient
from applicationinsights.flask.ext import AppInsights
from flask import current_app


class MonitoringService(object):
    def __init__(self, app=None):
        self.app = app
        self._client = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        config = current_app.config
        if config is not None:
            ikey = config['APPINSIGHTS_INSTRUMENTATIONKEY']
            if ikey: 
                self.client = TelemetryClient(ikey)
                self.client.context.application.ver = config['APP_VERSION']
                self.client.context.properties['iot_edge_module_name'] = config['APP_DESCRIPTION']
            else:
                self.client = DevAppInsight()

    def track_trace(self, trace_name, trace_object):
        self.client.track_trace(trace_name, trace_object)
        print('{} - {}'.format(trace_name, trace_object))
        self.client.flush()

    def track_metric(self, metric_name, metric_value):
        self.client.track_metric(metric_name, metric_value)
        print('{} - {}'.format(metric_name, metric_value))
        self.client.flush()

    def track_event(self, event_name, event_details):
        self.client.track_event(event_name, event_details)
        print('{} - {}'.format(event_name, event_details))
        self.client.flush()


class DevAppInsight: 
    def track_exception(self): 
        print('Oops! there was an exception')

    def track_trace(self, trace_name, trace_object):
        print('{} - {}'.format(trace_name, trace_object))

    def track_metric(self, metric_name, metric_value):
        print('{} - {}'.format(metric_name, metric_value))

    def track_event(self, event_name, event_details):
        print('{} - {}'.format(event_name, event_details))

    def flush(self):
        pass