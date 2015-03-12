Webite is a (hopefully) light Flask application setup using Docker and
Postgres. It takes ideas from [weber](https://github.com/vmalloc/weber/) but
tries to be lighter, maybe ill-advisedly. If you're familiar with Docker,
deployment should be easy with webite.

The Postgres backend for webite is a Docker postgres image, which can be
started with:

    docker run --name webite-db -e POSTGRES_USER=webite -e POSTGRES_PASSWORD=webite -v $(pwd)/persistent/db/:/var/lib/postgresql/data -p 15432:5432 -d postgres

Note the -v flag, which creates a folder called persistent to keep the database
around between containers. If the postgres container is deleted, the data will
persist there.

Flask-Migrate is included for easier alembic integration:

    export SQLALCHEMY_DATABASE_URI postgresql://webite:webite@localhost:15432/webite
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade

Webite uses Flask-Script for a test server and shell. To use the test server
with the Postgres container, do (in a Python environment matching the one in
the Dockerfile):

    python manage.py runserver

You should be up and running with a custom REST API for a Thing, running on
port 5000:

    curl http://127.0.0.1:5000/api/things/ -d "name=thing1" -X POST
    curl http://127.0.0.1:5000/api/things/1 -d "name=thing2" -X PUT

The Dockerfile sets up a production host that uses nginx to serve webite.

    docker build -t webite .
    docker run --name webite -p 8000:80 --link webite-db:db -d webite
