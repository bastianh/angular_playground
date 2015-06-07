import json
import logging
from flask import request, Response, abort, jsonify
from flask.ext.login import current_user, login_required
from sqlalchemy.orm import joinedload
from flask.ext.classy import FlaskView

from backend.utils.database import db
from backend.signals import on_init_app
from backend.models.todo import TodoModel, TodoSchema

todo_schema = TodoSchema()


def json_response(data=None, **kwargs):
    if data is None:
        data = {}
    if isinstance(data, dict) and len(kwargs):
        data.update(kwargs)
    response = Response(json.dumps(data), mimetype="application/json")
    return response

def get_response_json():
    req = request.get_json(cache=False)
    if not req:
        return abort(400, "missing json data")
    return req


# noinspection PyMethodMayBeStatic
class TodosView(FlaskView):
    decorators = [login_required]

    def get(self):
        todos = db.session.query(TodoModel).options(joinedload(TodoModel.creator)).all()
        return json_response(todo_schema.dump(todos, many=True).data)

    def post(self):
        req = get_response_json()
        obj = todo_schema.load(req).data
        obj.creator = current_user
        obj.save()
        return json_response(todo_schema.dump(obj).data)

    def delete(self, todo_id):
         todo = TodoModel.get_or_404(todo_id)
         todo.delete()
         return ""

        # def get(self, todo_id):
        #     abort_if_todo_doesnt_exist(todo_id)


        # def put(self, todo_id):
        #     parser = reqparse.RequestParser()
        #     parser.add_argument('task', type=str, help='Rate to charge for this resource')
        #     args = parser.parse_args()
        #     task = {'task': args['task']}
        #     TODOS[todo_id] = task
        #     return task, 201
        #     return TODOS[todo_id]


@on_init_app.connect
def init_app(app):

    @app.errorhandler(400)
    def bad_request(e):
        return json_response(error=e.code, name=e.name, description=e.description), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return json_response(error=e.code, name=e.name), 404

    TodosView.register(app)
