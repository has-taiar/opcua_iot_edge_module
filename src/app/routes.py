from app import api_bp, api, connector, monitor
from app.resources.node_controller import NodeController
from app.resources.nodes_get_controller import NodesGetController
from app.resources.nodes_set_controller import NodesSetController
from flask import current_app, request, Response
import json


api.add_resource(NodeController, '/node/<string:node_id>')
api.add_resource(NodesSetController, '/nodes/set')
api.add_resource(NodesGetController, '/nodes/get')


@api_bp.route('/')
def start():
    r = current_app.config['APP_DESCRIPTION']
    return Response(json.dumps(r), mimetype='application/json')
