from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT
from werkzeug.security import safe_str_cmp

from private_user import db , PrivateUserRegister,PrivateUserModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'behnam'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

def authenticate(username, password):
    user = PrivateUserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return PrivateUserModel.find_by_id(user_id)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(PrivateUserRegister, '/private_user_register')


if __name__ == '__main__':
    from private_user import db
    db.init_app(app)
    app.run(port=5000, debug=True)
