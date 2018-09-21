import time

from IPython import embed
from opcua import Client, crypto, ua

from app.opcua_utility import map_to_opcua_type_and_value
from flask import current_app


class OpcUaConnector(object):
    """The connector to OPC UA. This class manages all comms with DCS"""
    def __init__(self, app=None):
        self.app = app
        self._client = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        config = current_app.config
        if config is not None:
            self._server_address = config['OPC_SERVER_ADDRESS']
            self._client_name = config['OPC_CLIENT_NAME']
            self._client_description = config['OPC_CLIENT_DESCRIPTION']
            self._certificate_path = config['OPC_CERTIFICATE_PATH']
            self._private_key_path = config['OPC_PRIVATE_KEY_PATH']
            self._application_uri = config['OPC_APPLICATION_URI']
            self._max_time_out = config['OPC_MAX_TIME_OUT']
            self._client = None

    def _connect(self):
        self._client = Client(self._server_address, self._max_time_out)
        if (self._certificate_path is not None and self._private_key_path is not None):
            self._client.set_security(
                getattr(
                    crypto.security_policies, 'SecurityPolicy' + 'Basic256'),
                self._certificate_path, self._private_key_path,
                mode=getattr(ua.MessageSecurityMode, 'SignAndEncrypt'))
            self._client.application_uri = self._application_uri

        self._client.name = self._client_name
        self._client.description = self._client_description
        self._client.connect()
        # return _client

    def ensure_connection(self):
        if self._client is None:
            self._connect()

    def set_value(self, node_id, value_type_identifier, desired_value):
        """Set value on the OPC UA server. example parameters:
            Node_id=ns=4;s=node_name,
            value_type_identifier 0-25

            see: https://github.com/FreeOpcUa/python-opcua/blob/master/opcua/ua/uatypes.py#L619),
            desired_value could be any value that matches the UA Type
        """
        parsed_value, opc_type = map_to_opcua_type_and_value(
            value_type_identifier, desired_value)
        self.ensure_connection()
        node = self._client.get_node(node_id)
        dv = ua.DataValue(ua.Variant(parsed_value, opc_type))
        node.set_value(dv)

    def get_value(self, node_id):
        self.ensure_connection()
        node = self._client.get_node(node_id)
        value = node.get_value()
        return str(value)

    def disconnect(self):
        if self._client is not None:
            self._client.disconnect()
