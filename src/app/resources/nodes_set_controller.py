from flask_restful import Resource, Api
import json

from app import connector, monitor
from flask import request, Response


class NodesSetController(Resource):
    def post(self):
        result = {"is_successful": True}
        try:
            data = request.get_json()
            monitor.track_trace('opcua_iot_edge_module', {'request': 'POST', 'data': data})
            for node_id in list(data.keys()):
                print('node_id' + node_id + data[node_id]['type_identifier'] + data[node_id]['desired_value'])
                type_identifier = data[node_id]['type_identifier']
                desired_value = data[node_id]['desired_value'] 
                monitor.track_trace('opcua_iot_edge_module', 'Sending a request to OPC UA server with this details, node: \
                 {}, type_identifier: {}, desired_value: {}'.format(node_id, type_identifier, desired_value))
                connector.set_value(node_id, int(type_identifier), desired_value)
                
        except Exception as inst:
            monitor.client.track_exception()
            result = {"is_successful": False, "error": str(inst)}

        return Response(json.dumps(result), mimetype='application/json')