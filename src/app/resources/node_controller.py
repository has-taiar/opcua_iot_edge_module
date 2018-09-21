from flask_restful import Resource, Api
import json

from app import connector, monitor
from flask import current_app, request, Response


class NodeController(Resource):
    def get(self, node_id):
        result = {}
        try:
            monitor.track_trace('opcua_iot_edge_module', {'request': 'GET', 'node_id': node_id})
            result = connector.get_value(node_id)
        except Exception as inst:
            print(inst)
            current_app.logger.exception('{}'.format(inst))
            monitor.client.track_exception()
            result = {"error": str(inst)}

        return Response(json.dumps(result), mimetype='application/json')

    def post(self, node_id):
        result = {"is_successful": True}
        try:
            data = request.get_json()
            type_identifier = data['type_identifier']
            desired_value = data['desired_value']
            monitor.track_trace('opcua_iot_edge_module', {'request': 'POST', 'node_id': node_id, 'value_identifier': type_identifier, 'desired_value': desired_value})
            connector.set_value(node_id, int(type_identifier), desired_value)
        except Exception as inst:
            current_app.logger.exception('{}'.format(inst))
            monitor.client.track_exception()
            result = {"is_successful": False, "error": str(inst)}

        return Response(json.dumps(result), mimetype='application/json')