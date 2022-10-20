from flask import request
from flask_restx import Namespace, Resource

from dao.model.user import UserSchema
from implemented import user_service, auth_service
from tools import authentication_required

users_ns = Namespace('users')


@users_ns.route('/')
class UserView(Resource):
    @authentication_required
    def get(self):
        data_token = request.headers['Authorization']
        token = data_token.split("Bearer ")[-1]
        user = user_service.get_user_by_token(token)
        return UserSchema().dump(user), 200

    @authentication_required
    def patch(self):
        data = request.json
        data_token = request.headers['Authorization']
        token = data_token.split("Bearer ")[-1]
        user = user_service.get_user_by_token(token)
        data['id'] = user.id
        user_service.partical_update(data)
        return f"User {data['id']} updated", 204


@users_ns.route('/password')
class UserView(Resource):
    @authentication_required
    def put(self):
        data = request.json
        data_token = request.headers['Authorization']
        token = data_token.split("Bearer ")[-1]
        user = user_service.get_user_by_token(token)
        data['id'] = user.id
        auth_service.check_password(data)
        return 'Password updated', 204
