import jwt
from flask import request, abort, current_app


def authentication_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers.get('Authorization')
        token = data.split("Bearer ")[-1]
        print(token)
        try:
            jwt.decode(token, current_app.config['SECRET_KEY'], current_app.config['ALGO'])

        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper
