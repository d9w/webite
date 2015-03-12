# DOCKER-VERSION 0.11.1

FROM ubuntu:14.04

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-software-properties python3-pip python3-pycurl
RUN apt-get install -y software-properties-common curl wget ca-certificates libxml2-dev libxslt1-dev git supervisor libevent-dev libpq-dev redis-server
RUN apt-add-repository ppa:nginx/stable
RUN apt-get update
RUN apt-get install -y nginx

RUN pip3 install Flask-Mail Flask-Migrate>=1.3.0 Flask-SQLAlchemy Flask>=0.10.1 Flask-Script Logbook>=0.6.0 PyYAML URLObject alembic>=0.7.3 psycopg2 requests uwsgi

RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf
RUN rm -rf /etc/nginx/sites-enabled/*

ADD . /src
RUN ln -s /src/conf /conf
RUN ln -s /conf/app_nginx.conf /etc/nginx/sites-enabled/
RUN ln -s /conf/app_supervisor.conf /etc/supervisor/conf.d/

ENV CONFIG_DIRECTORY /conf/
ENV SQLALCHEMY_DATABASE_URI postgresql+psycopg2://webite:webite@$DB_PORT_5432_TCP_ADDR:$DB_PORT_5432_TCP_PORT/webite

EXPOSE 80
CMD ["supervisord", "-n"]
