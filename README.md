# OPC UA IoT Edge Module
This is a simple and lightweight IoT Edge module that can be used to integrate with DCS/SCADA systems using OPC UA protocol. The module allows you read and write one or many values (tags) from and to these systems. 

## Getting Started
You can just pull the docker container locally and run it like so: 

```
$ docker pull docker pull hasaltaiar/opcua_iot_edge_module
```
This will pull the image locally. You can then run the docker container locally with the following parameters (or use docker compose with .env file as provided).

```
$ docker run -it -p 5000:80 -e OPC_SERVER_ADDRESS="opc_ua_server_with_port_and_path" -e OPC_CLIENT_NAME="IoT_Edge_Python" -e OPC_CLIENT_DESCRIPTION="IoT_Edge_Python" -e APP_HOST=0.0.0.0 -e APP_PORT=5000 -e NGINX_PORT=80 -e LOG_LEVEL=debug hasaltaiar/opcua_iot_edge_module
```
The command above will start the docker container and make it available on port `5000`. You can then start using postman to read/write values. 
This assumes that you are providing only username and passwords in the server address. The module also allows you to generate and add certificate. If you do so, the module will use these certificate and will `SignAndEncrypt` all comms as supported by OPC UA. 

## List of all ENV Variables
You do not have to pass all. The mandatory ones are listed in the `docker run` command above. 

```xml
OPC_SERVER_ADDRESS=opc.tcp://username:password@192.168.100.100:53530/OPCUA/SimulationServer
OPC_CLIENT_NAME=IoTEdgeModule
OPC_CLIENT_DESCRIPTION=IoTEdgeModule
OPC_CERTIFICATE_PATHs=../certs/cert_iot_edge.der  # optional
OPC_PRIVATE_KEY_PATHs=../certs/cert_iot_edge.pem  # optional 
APP_HOST=127.0.0.1
APP_PORT=5000
NGINX_PORT=80
OPC_APPLICATION_URI=urn:IoTEdge  # optional 
```

If you wanted all comms to be `SignAndEncrypt`-ed, then you need to generate certificates (with private key). When generating these certificates you need to add your `application_uri` into the certificate attibutes. The module checks if the `OPC_APPLICATION_URI` is passed, it assumes that there are certificates provided with an attribute that matches this `application_uri`. If you do not want to `SignAndEncrypt` everything, then just start with the username and password. Starting the testing with username and password only is probably a good way to start. 

## Getting Started with Dev

You can clone the repo locally if you want to do development or change something. Then you can spin up the whole environement using one of these 2 options: 

### Option 1: Using Conda Manually. 
Once you have the repo local, navigate to the repo folder and create your python virtual environment using conda. (You need to make sure that conda is there on your dev box)

```sh
$ conda env create -f environment.yml
$ conda activate iot_edge_module_opc_control
```

### Option 2: Using Docker Compose
Once you have the repo locally and navigated into the folder, then just do docker compose up: 

```sh
$ docker-compose up --build
```
This will build the whole environment and you can start playing with it. 

# Build and Test

This project has both [pytest](https://pytest.readthedocs.io/en/reorganize-docs/example/index.html) and [coverage](https://coverage.readthedocs.io) installed.

To run all unit tests:

```sh
# navigate to the repo folder, then run all tests
$ pytest
```

To view a coverage report:

```
$ coverage run -m pytest

$ coverage report

# For a more in-depth coverage report in html and interactive javascript:

$ coverage run -m pytest

$ coverage html
```

Then navigate to `htmlcov/index.html` in your browser to see exactly which
lines have been covered by the unit tests.

The `APPINSIGHTS_INSTRUMENTATIONKEY` only needs to be set for sending telemetry and errors in prod. Not needed for DEV or TEST env. To get the instrumentation key for the prod, follow the instruction on the [MSDN](https://docs.microsoft.com/en-us/azure/application-insights/app-insights-create-new-resource) doc. 

# Software Dependencies

## OPC UA Simulator
To do some development and testing, you can use a tool to simulate OPC UA server and interact with it. The one I used for developing this was the one from ProSys

- Download and install the [Windows client](https://www.prosysopc.com/opcua/apps/JavaClient/dist/3.1.4-293/prosys-opc-ua-client-3.1.4-293.exe)
- Download and install the [Winodws server](https://www.prosysopc.com/opcua/apps/JavaServer/dist/3.1.4-175/prosys-opc-ua-simulation-server-3.1.4-175.exe)
- Run the server
    - Goto Users tab: Create user `dev` (password: `dev`)
    - Goto Endpoints tab: Copy `UA TCP` value into -> `OPC_SERVER_ADDRESS`
    - Goto Simulation
        - Dropdown Signal Type: Select Counter
        - NodeId/Name: `dev`
        - Click Create
        - In left window click the new Signa Name and view the attributes
    - Goto Address Space:
        - Objects > Simulation > dev
        - Copy selected values of the attribute `NodeId`
        - e.g. `ns=5;s=dev`


<!-- ## IoT Hub Setup
moduleName: opcua_iot_edge_module
repo url: hasaltaiar/opcua_iot_edge_module
```json
{
	"ExposedPorts":{"80/tcp": {}},
	"HostConfig": {
		"PortBindings": {
			"80/tcp": [
				{
				"HostPort": "5000"
				}
				]
		}
	}
}
``` -->

# API references

## Reading ONE value from the OPC UA
```
POST http://localhost:5000/api/v1/node/ns=5;s=val2

# Sample response payload
"hello World"
```

## Writing ONE value to the OPC UA
```
POST http://localhost:5000/api/v1/node/ns=5;s=val1

# Sample request payload
{ 
	"type_identifier": "6", 
    "desired_value" "6666"
}

# Sample response payload
{
    "is_successful": true,
    "error": null
}
```

## Reading Multiple  values from the OPC UA
```
POST http://localhost:5000/api/v1/nodes/get

# Sample request
{ 
	"node_ids": ["ns=5;s=val1", "ns=5;s=val2"]
}

# Sample response payload
{
    "ns=5;s=val2": "19",
    "ns=5;s=val1": "19"
}
```

## Writing Mutliple values to the OPC UA
```
POST http://localhost:5000/api/v1/nodes/set

# Sample request payload
{
	"ns=5;s=val1": {"type_identifier": "6", "desired_value": "555"},  
	"ns=5;s=val2": {"type_identifier": "6", "desired_value": "8888"}
}

# Sample response payload
{
    "is_successful": true,
    "error": null
}
```