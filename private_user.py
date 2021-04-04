import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class PrivateUserRegisterModel():
    TABLE_NAME = 'private_users'

    def __init__(self, _id, username, password,email_address,full_name,date_of_birth,mobile_number):
        self.id = _id
        self.username = username
        self.password = password
        self.email_address=email_address
        self.full_name=full_name
        self.date_of_birth=date_of_birth
        self.mobile_number=mobile_number

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('users_database.db')
        cursor = connection.cursor()
        query = "SELECT * FROM private_users WHERE username=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            private_users = cls(*row)
        else:
            private_users = None
        connection.close()
        return private_users

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('users_database.db')
        cursor = connection.cursor()
        query = "SELECT * FROM private_users WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            private_users = cls(*row)
        else:
            private_users = None
        connection.close()
        return private_users


class PrivateUserRegister(Resource):
    TABLE_NAME = 'private_users'

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('email_address',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('full_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('date_of_birth',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('mobile_number',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data=PrivateUserRegister.parser.parse_args()
        if PrivateUserRegisterModel.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400
        connection = sqlite3.connect('users_database.db')
        cursor = connection.cursor()
        query = "INSERT INTO private_users VALUES (NULL, ?, ?,?,?,?,?)".format(table=self.TABLE_NAME)
        cursor.execute(query, (data['username'], data['password'],data['email_address'],data['full_name'],data['date_of_birth'],data['mobile_number']))
        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201


class PrivateUserList(Resource):
    TABLE_NAME = 'private_users'

    @jwt_required()
    def get(self, username):
        private_user_date = self.find_by_user_name(username)
        if private_user_date:
            return private_user_date
        return {'message': 'user not found'}, 404

    @classmethod
    def find_by_user_name(cls, username):
        connection = sqlite3.connect('users_database.db')
        cursor = connection.cursor()

        query = "SELECT * FROM private_users WHERE username=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'User Data are': {'Username': row[1], 'Email Address': row[3],'Full Name':row[4],'Date Of Birth':row[5],'Mobile Number:':row[6]}}

    def post(self, username):
        if self.find_by_user_name(username):
            return { "A user with name '{}' already exists.".format(username)}

        data = PrivateUserRegister.parser.parse_args()

        private_user_data = {'username': username, 'email_address': data['email_address'],'full_name': data['full_name'],'date_of_birth': data['date_of_birth'],'mobile_number': data['mobile_number']}

        try:
            PrivateUserRegister.insert(private_user_data)
        except:
            return { "An error occurred inserting the user data."}

        return private_user_data



    @classmethod
    def insert(cls, data):
        connection = sqlite3.connect('users_database.db')
        cursor = connection.cursor()

        query = "INSERT INTO private_users VALUES(?,?,?,?,?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (data['username'],data['email_address'],data['full_name'],data['date_of_birth'],data['mobile_number']))

        connection.commit()
        connection.close()

    @jwt_required()
    def put(self, username):
        data = PrivateUserRegister.parser.parse_args()
        private_user_data = self.find_by_user_name(username)
        updated_item = {'username':username,'email_address':data['email_address'],'full_name':data['full_name'],'date_of_birth':data['date_of_birth'],'mobile_number':data['mobile_number']}
        if private_user_data is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the data."}
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occurred updating the item."}
        return updated_item

    @classmethod
    def update(cls, data):
        connection = sqlite3.connect('users_database.db')
        cursor = connection.cursor()

        query = "UPDATE private_users SET email_address=? WHERE username=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (data['email_address'],data['username']))

        query = "UPDATE private_users SET full_name=? WHERE username=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (data['full_name'], data['username']))

        query = "UPDATE private_users SET date_of_birth=? WHERE username=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (data['date_of_birth'], data['username']))

        query = "UPDATE private_users SET mobile_number=? WHERE username=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (data['mobile_number'], data['username']))

        



        connection.commit()
        connection.close()

    @jwt_required()
    def delete(self, username):
        connection = sqlite3.connect('users_database.db')
        cursor = connection.cursor()

        query = "DELETE FROM private_users WHERE username=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (username,))

        connection.commit()
        connection.close()

        return {'message': 'user deleted successfully'}