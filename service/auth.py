import base64
import calendar
import datetime
import hashlib
import hmac

import jwt
from flask_restx import abort

from constant import ALGO, PWD_HASH_SALT, PWD_HASH_ITERATIONS, SECRET_HERE
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

        data = {'email': user.email,
                'role': user.role}

        min30 = datetime.datetime.utcnow() + datetime.timedelta(seconds=1)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET_HERE, algorithm=ALGO)
        d30 = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        data['exp'] = calendar.timegm(d30.timetuple())
        refresh_token = jwt.encode(data, SECRET_HERE, algorithm=ALGO)

        return {'access_token': access_token,
                'refresh_token': refresh_token}

    def approve_refresh_tokens(self, token):
        try:
            data = jwt.decode(jwt=token, key=SECRET_HERE, algorithms=[ALGO])
            email = data.get('email')
            return self.generate_token(email, None, is_refresh=True)

        except Exception:
            abort(401)

    def compare_paswords(self, db_password, json_password):
        return hmac.compare_digest(
            base64.b64decode(db_password),
            hashlib.pbkdf2_hmac(
                'sha256',
                json_password.encode('utf-8'),
                PWD_HASH_SALT,
                PWD_HASH_ITERATIONS))
