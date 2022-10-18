from flask import request, abort
from flask_restx import Namespace, Resource

from implemented import user_service, auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/register/')
class AuthView(Resource):
    def post(self):
        data = request.json
        user_service.create_user(data)
        return f'User {data.get("email")} created'


@auth_ns.route('/login/')
class AuthView(Resource):
    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')
        if None in [email, password]:
            abort(400)
        tokens = auth_service.generate_token(email, password)
        return tokens, 201

    def put(self):
        data = request.json
        token = data.get('refresh_token')
        tokens = auth_service.approve_refresh_tokens(token)
        return tokens, 201
