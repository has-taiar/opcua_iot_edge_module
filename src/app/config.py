import os
import re

from dotenv import load_dotenv, find_dotenv
from .__about__ import __description__, __version__

load_dotenv(find_dotenv())

# find api semver MAJOR
find = re.compile(r"([^.]*)")
api_version = 'v' + re.search(find, __version__).group(0)


class Config(object):
    API_VERSION = api_version
    APP_DESCRIPTION = __description__
    APP_VERSION = __version__
    LOG_LEVEL = os.environ['LOG_LEVEL']

    # mandatory for using the server sim
    # see: README for more info
    OPC_SERVER_ADDRESS = os.environ.get('OPC_SERVER_ADDRESS')
    OPC_CLIENT_NAME = os.environ.get('OPC_CLIENT_NAME')
    OPC_CLIENT_DESCRIPTION = os.environ.get('OPC_CLIENT_DESCRIPTION')

    # optional for using the server sim
    # see: README for more info
    OPC_CERTIFICATE_PATH = os.environ.get('OPC_CERTIFICATE_PATH')
    OPC_PRIVATE_KEY_PATH = os.environ.get('OPC_PRIVATE_KEY_PATH')
    OPC_APPLICATION_URI = os.environ.get('OPC_APPLICATION_URI')
    APPINSIGHTS_INSTRUMENTATIONKEY = os.environ.get('APPINSIGHTS_INSTRUMENTATIONKEY')
    # 5min timeout for OpcConnector class
    OPC_MAX_TIME_OUT = 300
    # App settings
    APP_HOST = os.environ.get('APP_HOST')
    APP_PORT = os.environ.get('APP_PORT')
    APP_HOST_PORT = '{}:{}'.format(os.environ.get('APP_HOST'), os.environ.get('APP_PORT'))

