from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from werkzeug.security import safe_str_cmp
from private_user import PrivateUserRegister,PrivateUserList,PrivateUserRegisterModel
from business_user import BusinessUserRegister,BusinessUserList,BusinessUserRegisterModel

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'behnam'
api = Api(app)



def authenticate_private_user(username, password):
    user = PrivateUserRegisterModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity_private_user(payload):
    user_id = payload['identity']
    return PrivateUserRegisterModel.find_by_id(user_id)

def authenticate_business_user(username, password):
    user = BusinessUserRegisterModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity_business_user(payload):
    user_id = payload['identity']
    return BusinessUserRegisterModel.find_by_id(user_id)

jwt_private_user = JWT(app, authenticate_private_user, identity_private_user)  # /auth

jwt_business_user=JWT(app, authenticate_business_user, identity_business_user)  # /auth

api.add_resource(PrivateUserRegister, '/private_user_register')
api.add_resource(PrivateUserList, '/private_user/<string:username>')

api.add_resource(BusinessUserRegister, '/business_user_register')
api.add_resource(BusinessUserList, '/business_user/<string:username>')



if __name__ == '__main__':

    app.run(port=5000, debug=True)
