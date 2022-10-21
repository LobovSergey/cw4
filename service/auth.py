import base64
import calendar
import datetime
import hashlib
import hmac

import jwt
from flask import current_app
from flask_restx import abort

from service.user import UserService


class AuthService:

    def __init__(self, service: UserService):
        self.service = service

    def generate_token(self, email, password, is_refresh=False):

        user = self.service.get_by_username(email)
        if user is None:
            raise abort(404)

        if not is_refresh:
            if not self.compare_paswords(user.password, password):
                raise abort(400)

        data = {'email': user.email}

        access_time = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
        data['exp'] = calendar.timegm(access_time.timetuple())
        access_token = jwt.encode(data, current_app.config['SECRET_KEY'], algorithm=current_app.config['ALGO'])
        refresh_time = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config['TOKEN_EXPIRE_DAYS'])
        data['exp'] = calendar.timegm(refresh_time.timetuple())
        refresh_token = jwt.encode(data, current_app.config['SECRET_KEY'], algorithm=current_app.config['ALGO'])

        return {'access_token': access_token,
                'refresh_token': refresh_token}

    def approve_refresh_tokens(self, token):
        data = jwt.decode(jwt=token, key=current_app.config['SECRET_KEY'], algorithms=current_app.config['ALGO'])
        email = data.get('email')
        return self.generate_token(email, None, is_refresh=True)

    def compare_paswords(self, db_password, json_password):
        return hmac.compare_digest(
            base64.b64decode(db_password),
            hashlib.pbkdf2_hmac(
                'sha256',
                json_password.encode('utf-8'),
                current_app.config['PWD_HASH_SALT'],
                current_app.config['PWD_HASH_ITERATIONS']))

    def check_password(self, data):
        if data.get('password_1') is None or data.get('password_2') is None:
            abort(404)

        if not self.compare_paswords(data.get("password_db"), data.get('password_1')):
            abort(401)

        self.service.update_password(data)
