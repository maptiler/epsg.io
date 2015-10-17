FROM klokantech/gdal:1.11

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -qq update \
&& apt-get -qq -y --no-install-recommends install curl \
&& curl https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py | python \
&& mkdir -p /var/www

COPY . /var/www/epsg.io
WORKDIR /var/www/epsg.io

VOLUME /var/www/epsg.io

RUN pip install -q -r requirements.txt

EXPOSE 8080

CMD gunicorn --workers 4 --bind 127.0.0.1:8080 --log-level info app:app