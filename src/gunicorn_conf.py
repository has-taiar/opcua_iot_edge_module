# http://docs.gunicorn.org/en/stable/configure.html#configuration-file
# http://docs.gunicorn.org/en/stable/settings.html#config-file
import logging
import os

accesslog = '-'
bind = os.environ['APP_HOST'] + ':' + os.environ['APP_PORT']
errorlog = '-'
loglevel = os.environ['LOG_LEVEL']
loglevel = 'debug' if os.environ['LOG_LEVEL'] == 'trace' else loglevel
pythonpath = '/opt/bin/conda;/app'
workers = 1


def pre_request(worker, req):
    worker.log.debug("%s %s" % (req.method, req.path))

