FROM hasaltaiar/ubuntu_miniconda3:latest

# Install gunicorn supervisor
RUN apt-get update \
    && apt-get install -y nginx supervisor libcurl4-openssl-dev libboost-python-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install flask and environment
COPY environment.yml /app/environment.yml

RUN conda env update -f /app/environment.yml -n base --prune

# Setup gunicorn and nginx
COPY flask.conf /etc/nginx/sites-available/
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN rm /etc/nginx/sites-enabled/default \
    && ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf \
    && echo "daemon off;" >> /etc/nginx/nginx.conf \
    && mkdir -p /var/log/supervisor

RUN mkdir -p /app
COPY /src /app

RUN mkdir -p /certs
COPY /certs/ /certs/

CMD ["/usr/bin/supervisord"]