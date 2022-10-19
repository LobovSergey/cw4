import base64
import hashlib

import jwt
from flask import current_app

from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def create_user(self, data):
        password_data = data.get('password')
        data['password'] = self.get_hash_password(password_data)

        return self.dao.create_user(data)

    def get_by_username(self, username):
        return self.dao.get_by_name(username)

    def get_hash_password(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256', password.encode('utf-8'),
            current_app.config['PWD_HASH_SALT'],
            current_app.config['PWD_HASH_ITERATIONS'])
        return base64.b64encode(hash_digest)

    def get_user_by_token(self, token):
        decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'],
                                   algorithms=[current_app.config['ALGO']])
        user_email = decoded_token.get("email")

        return self.dao.get_by_name(user_email)
