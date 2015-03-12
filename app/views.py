from flask import jsonify, request, abort
from flask.views import MethodView

from .app import app
from .models import db, Thing
from .methodviews import ThingListAPI, ThingAPI

@app.route('/')
def hello_world():
    config = {}
    for key in app.config.keys():
        config[key] = str(app.config[key])
    return jsonify(config)

app.add_url_rule('/api/things/', view_func=ThingListAPI.as_view('thing_list_api'),
        methods=['GET','POST'])

app.add_url_rule('/api/things/<int:thing_id>', view_func=ThingAPI.as_view('thing_api'),
        methods=['GET','PUT','DELETE'])

