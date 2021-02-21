from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

USERS = {
    "0": {'name': 'Humberto'},
    "1": {'name': 'Doisberto'},
    "2": {'name': 'Tresberto'},
}


def abort_if_todo_doesnt_exist(user_id):
    if user_id not in USERS:
        abort(404, message="User {} doesn't exist".format(user_id))

parser = reqparse.RequestParser()
parser.add_argument('name')


class User(Resource):
    def get(self, user_id):
        abort_if_todo_doesnt_exist(user_id)
        return USERS[user_id]

    def delete(self, user_id):
        abort_if_todo_doesnt_exist(user_id)
        del USERS[user_id]
        return '', 204

    def put(self, user_id):
        args = parser.parse_args()
        name = {'name': args['name']}
        USERS[user_id] = name
        return name, 201


class UserList(Resource):
    def get(self):
        return USERS

    def post(self):
        args = parser.parse_args()
        user_id = str(int(max(USERS.keys())) + 1)
        USERS[user_id] = {'name': args['name']}
        return USERS[user_id], 201

api.add_resource(UserList, '/users/')
api.add_resource(User, '/users/<user_id>')


if __name__ == '__main__':
    app.run(debug=True)