# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import random
import time
import sys
import iothub_client
from iothub_client import IoTHubModuleClient, IoTHubClientError, IoTHubTransportProvider
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError

from config import Config

# messageTimeout - the maximum time in milliseconds until a message times out.
# The timeout period starts at IoTHubModuleClient.send_event_async.
# By default, messages do not expire.
MESSAGE_TIMEOUT = 10000

# global counters
RECEIVE_CALLBACKS = 0
SEND_CALLBACKS = 0
TEMPERATURE_THRESHOLD = 25
TWIN_CALLBACKS = 0

# global nodes addresses and tags
# PI_TAGS = ["SOMETHING.PV","SOMETHINGELSE.PV"]
# OPCUA_ADDRESS = ["ns=4;s=Float","ns=4;s=Int64"]

# Choose HTTP, AMQP or MQTT as transport protocol.  Currently only MQTT is supported.
PROTOCOL = IoTHubTransportProvider.MQTT


# Callback received when the message that we're forwarding is processed.
def send_confirmation_callback(message, result, user_context):
    global SEND_CALLBACKS
    print("Confirmation[%d] received for message with result = %s" % (user_context, result) )
    map_properties = message.properties()
    key_value_pair = map_properties.get_internals()
    print("    Properties: %s" % key_value_pair )
    SEND_CALLBACKS += 1
    print("    Total calls confirmed: %d" % SEND_CALLBACKS )


# receive_message_callback is invoked when an incoming message arrives on the specified 
# input queue (in the case of this sample, "input1").  Because this is a filter module, 
# we forward this message to the "output1" queue.
def receive_message_callback(message, hubManager):
    global RECEIVE_CALLBACKS
    global TEMPERATURE_THRESHOLD
    message_buffer = message.get_bytearray()
    size = len(message_buffer)
    message_text = message_buffer[:size].decode('utf-8')
    print("    Data: <<<%s>>> & Size=%d" % (message_text, size))
    map_properties = message.properties()
    key_value_pair = map_properties.get_internals()
    print("    Properties: %s" % key_value_pair)
    RECEIVE_CALLBACKS += 1
    print("    Total calls received: %d" % RECEIVE_CALLBACKS)
    data = json.loads(message_text)

    if "node_id" in data and "desired_value" in data and "type_identifier" in data:
        node_id = data["node_id"]
        desired_value = data["desired_value"]
        value_type_identifier = data["type_identifier"]
        connector = OpcUaConnector(Config())
        connector.set_value(node_id, int(value_type_identifier), desired_value)

    # # work with the data coming in
    # if "machine" in data and "temperature" in data["machine"] and data["machine"]["temperature"] > TEMPERATURE_THRESHOLD:
    #     map_properties.add("MessageType", "Alert")
    #     print("Machine temperature %s exceeds threshold %s" % (data["machine"]["temperature"], TEMPERATURE_THRESHOLD))

    hubManager.forward_event_to_output("output1", message, 0)
    return IoTHubMessageDispositionResult.ACCEPTED


class HubManager(object):

    def __init__(
            self,
            protocol=IoTHubTransportProvider.MQTT):
        self.client_protocol = protocol
        self.client = IoTHubModuleClient()
        self.client.create_from_environment(protocol)

        # Sets the callback when a module twin's desired properties are updated.
        self.client.set_module_twin_callback(module_twin_callback, self)

        # set the time until a message times out
        self.client.set_option("messageTimeout", MESSAGE_TIMEOUT)
        
        # sets the callback when a message arrives on "input1" queue.  Messages sent to 
        # other inputs or to the default will be silently discarded.
        self.client.set_message_callback("input1", receive_message_callback, self)

    # Forwards the message received onto the next stage in the process.
    def forward_event_to_output(self, outputQueueName, event, send_context):
        self.client.send_event_async(
            outputQueueName, event, send_confirmation_callback, send_context)

# module_twin_callback is invoked when the module twin's desired properties are updated.
def module_twin_callback(update_state, payload, user_context):
    global TWIN_CALLBACKS
    global TEMPERATURE_THRESHOLD
    global PI_TAGS
    global OPCUA_ADDRESS

    print("\nTwin callback called with:\nupdateStatus = %s\npayload = %s\ncontext = %s" % (update_state, payload, user_context) )
    data = json.loads(payload)
    
    # # When properties updated
    # if "desired" in data and "pi_tag_opcua_mapping" in data["desired"]:
    #     if "pi_tags" in data["desired"]["pi_tag_opcua_mapping"] and "opcua_addresses" in data["desired"]["pi_tag_opcua_mapping"]:
    #         PI_TAGS = list(data["desired"]["pi_tag_opcua_mapping"]["pi_tags"])
    #         OPCUA_ADDRESS = list(data["desired"]["pi_tag_opcua_mapping"]["opcua_addresses"])
            
    #         if len(PI_TAGS) != len(OPCUA_ADDRESS):
    #             print("Pi Tag and OPC UA addresses do not have the same amount of values")
    #             return
    #     else:
    #         print("Pi Tags and OPC UA addresses not correctly defined.")
    #         return

    TWIN_CALLBACKS += 1
    print("Total calls confirmed: %d\n" % TWIN_CALLBACKS)


def main(protocol):
    try:
        print("\nPython %s\n" % sys.version)
        print("IoT Hub Client for Python")

        hub_manager = HubManager(protocol)

        print("Starting the IoT Hub Python sample using protocol %s..." % hub_manager.client_protocol)
        print("The sample is now waiting for messages and will indefinitely.  Press Ctrl-C to exit. ")

        while True:
            time.sleep(1)

    except IoTHubError as iothub_error:
        print("Unexpected error %s from IoTHub" % iothub_error)
        return
    except KeyboardInterrupt:
        print("IoTHubModuleClient sample stopped")


if __name__ == '__main__':
    # while True:
    #     print('Entered edge main', flush=True)
    #     time.sleep(5)
    main(PROTOCOL)
