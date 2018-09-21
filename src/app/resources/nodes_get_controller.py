from flask_restful import Resource, Api
import json

from app import connector, monitor
from flask import request, Response


class NodesGetController(Resource):
    def post(self):
        result = {}
        try:
            data = request.get_json()
            monitor.track_trace('opcua_iot_edge_module', {'request': 'GET', 'node_ids': data})
            for node in data['node_ids']:
                opcua_value = connector.get_value(node)
                result[node] = opcua_value
        except Exception as inst:
            print(inst)
            monitor.client.track_exception()
            result = {"error": str(inst)}

        return Response(json.dumps(result), mimetype='application/json')