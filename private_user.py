from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

db =SQLAlchemy()


class PrivateUserModel(db.Model):
    __tablename__ = 'private_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


class PrivateUserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = PrivateUserRegister.parser.parse_args()

        if PrivateUserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = PrivateUserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201