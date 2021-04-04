import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class BusinessUserRegisterModel():
    TABLE_NAME = 'business_users'

    def __init__(self, _id, username, password, email_address, owner, business_name,business_address ,telephone_number,mobile_number):
        self.id = _id
        self.username = username
        self.password = password
        self.email_address = email_address
        self.owner = owner
        self.business_name = business_name
        self.business_address=business_address
        self.telephone_number=telephone_number
        self.mobile_number = mobile_number

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('users_database.db')
        cursor = connection.cursor()
        query = "SELECT * FROM business_users WHERE username=?".format(table=cls.TABLE_NAME)
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
        query = "SELECT * FROM business_users WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            private_users = cls(*row)
        else:
            private_users = None
        connection.close()
        return private_users


class BusinessUserRegister(Resource):
    TABLE_NAME = 'business_users'

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
    parser.add_argument('owner',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('business_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('business_address',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('telephone_number',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('mobile_number',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = BusinessUserRegister.parser.parse_args()
        if BusinessUserRegisterModel.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400
        connection = sqlite3.connect('users_database.db')
        cursor = connection.cursor()
        query = "INSERT INTO business_users VALUES (NULL, ?, ?,?,?,?,?,?,?)".format(table=self.TABLE_NAME)
        cursor.execute(query, (
        data['username'], data['password'], data['email_address'], data['owner'], data['business_name'],
        data['business_address'],data['telephone_number'],data['mobile_number']))
        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201


class BusinessUserList(Resource):
    TABLE_NAME = 'business_users'

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

        query = "SELECT * FROM business_users WHERE username=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'User Data are': {'Username': row[1], 'Email Address': row[3], 'Business Owner': row[4],
                                      'Business Name': row[5], 'Business Address:': row[6], 'Telephone Number:':row[7],'Mobile Number:':row[8]}}

    def post(self, username):
        if self.find_by_user_name(username):
            return {"A user with name '{}' already exists.".format(username)}

        data = BusinessUserRegister.parser.parse_args()

        business_user_data = {'username': username, 'email_address': data['email_address'],
                             'full_name': data['full_name'], 'date_of_birth': data['date_of_birth'],
                             'mobile_number': data['mobile_number']}

        try:
            BusinessUserRegister.insert(business_user_data)
        except:
            return {"An error occurred inserting the user data."}

        return business_user_data

    @classmethod
    def insert(cls, data):
        connection = sqlite3.connect('users_database.db')
        cursor = connection.cursor()

        query = "INSERT INTO business_users VALUES(?,?,?,?,?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (
        data['username'], data['email_address'], data['full_name'], data['date_of_birth'], data['mobile_number']))

        connection.commit()
        connection.close()

    @jwt_required()
    def put(self, username):
        data = BusinessUserRegister.parser.parse_args()
        business_user_data = self.find_by_user_name(username)
        updated_item = {'username': username, 'email_address': data['email_address'], 'owner': data['owner'],
                        'business_name': data['business_name'], 'business_address': data['business_address'],'telephone_number':data['telephone_number'],'mobile_number':data['mobile_number']}
        if business_user_data is None:
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

        query = "UPDATE business_users SET email_address=? WHERE username=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (data['email_address'], data['username']))

        query = "UPDATE business_users SET owner=? WHERE username=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (data['owner'], data['username']))

        query = "UPDATE business_users SET business_name=? WHERE username=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (data['business_name'], data['username']))

        query = "UPDATE business_users SET business_address=? WHERE username=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (data['business_address'], data['username']))

        query = "UPDATE business_users SET telephone_number=? WHERE username=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (data['telephone_number'], data['username']))

        query = "UPDATE business_users SET mobile_number=? WHERE username=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (data['mobile_number'], data['username']))

        connection.commit()
        connection.close()

    @jwt_required()
    def delete(self, username):
        connection = sqlite3.connect('users_database.db')
        cursor = connection.cursor()

        query = "DELETE FROM business_users WHERE username=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (username,))

        connection.commit()
        connection.close()

        return {'message': 'user deleted successfully'}