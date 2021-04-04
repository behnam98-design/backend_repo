import sqlite3

connection=sqlite3.connect("users_database.db")
cursor=connection.cursor()

private_users="CREATE TABLE IF NOT EXISTS private_users (id INTEGER PRIMARY KEY, username text, password text ," \
                    "email_address text, full_name text, date_of_birth int,mobile_number int) "
cursor.execute(private_users)

business_user="CREATE TABLE IF NOT EXISTS business_users (id INTEGER PRIMARY KEY, username text, password text ," \
                    "email_address text,owner text ,business_name text,business_address text ,telephone_number int," \
              "mobile_number int) "
cursor.execute(business_user)


connection.commit()
cursor.close()

