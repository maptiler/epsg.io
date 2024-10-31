FROM klokantech/gdal:1.11

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -qq update \
&& apt-get -qq -y --no-install-recommends install curl \
&& curl https://bootstrap.pypa.io/pip/2.7/get-pip.py | python \
&& mkdir -p /var/www

COPY requirements.txt /tmp/requirements.txt
RUN pip install -q -r /tmp/requirements.txt

COPY . /var/www/epsg.io
VOLUME /var/www/epsg.io
WORKDIR /var/www/epsg.io

EXPOSE 8000
ENV FLASK_APP=/var/www/epsg.io/app.py
