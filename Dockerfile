FROM python:3.10.5-slim-buster

# ENV DEBIAN_FRONTEND noninteractive

# TODO remove GDAL related bloatware and build tools

RUN apt-get -qq update \
&& apt-get -qq -y --no-install-recommends install build-essential python3-distutils curl gdal-bin libgdal-dev \
&& curl https://bootstrap.pypa.io/get-pip.py | python \
&& mkdir -p /var/www

COPY requirements.txt /tmp/requirements.txt
RUN pip install setuptools==57.5.0
RUN pip install -q -r /tmp/requirements.txt


# COPY . /var/www/epsg.io
VOLUME /var/www/epsg.io
WORKDIR /var/www/epsg.io

EXPOSE 8000
ENV FLASK_APP=/var/www/epsg.io/app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

