from flask import jsonify, request, abort
from flask.views import MethodView

from .app import app
from .models import db, Thing

def get_or_404(model, id):
    rv = model.query.get(id)
    if rv is None:
        abort(404, "%s %s does not exist" % (model.__name__, str(id)))
    return rv

class ThingListAPI(MethodView):

    def get(self):
        things = Thing.query.all()
        return jsonify(dict(items=[thing.config() for thing in things]))

    def post(self):
        if set(['name']) > set(request.form.keys()):
            abort(400, "Things need names")
        thing = Thing(name=request.form.get('name'))
        db.session.add(thing)
        db.session.commit()
        return jsonify(thing.config())

class ThingAPI(MethodView):

    def get(self, thing_id):
        thing = get_or_404(Thing, thing_id)
        return jsonify(thing.config())

    def put(self, thing_id):
        thing = get_or_404(Thing, thing_id)
        if 'name' in request.form:
            thing.name = request.form.get('name')
        db.session.add(thing)
        db.session.commit()
        return jsonify(thing.config())

    def delete(self, thing_id):
        thing = get_or_404(Thing, thing_id)
        db.session.delete(thing)
        db.session.commit()
        return jsonify(dict(items=[thing.config() for thing in Thing.query.all()]))


