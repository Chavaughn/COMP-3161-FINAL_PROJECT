from flask import jsonify, request
from app.controllers.AppController import *
from werkzeug.security import generate_password_hash

from app.json_messages import *

# *****************Register*****************
@app.route('/register', methods=['POST', 'GET'])
def register_postman():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    password = generate_password_hash(request.json['password'], method='pbkdf2:sha256')
    account_type = request.json['account_type']
    last_username = 0
    if current_user.is_authenticated:
        flash('User is already logged in.', 'info')
        return redirect(url_for('landing'))
    with open('./app/sql/students/getLastUsername.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            last_username = db.session.execute(text(sql_script)).first()[0]
    username = last_username + 1
    email = f"{username}@mymona.uwi.edu"
    with open('./app/sql/accounts/registerAccount.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
             db.session.execute(text(sql_script),  
                                {
                            "username": username,
                            "first_name":first_name,
                            "last_name":last_name,
                            "password": password,
                            "email":email,
                            "account_type":account_type
                           })
             db.session.commit()

    with open('./app/sql/accounts/getAccount.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
             user = db.session.execute(text(sql_script),  {"username": username}).first()
    if (account_type == 2):
        #register lecturer
        with open('./app/sql/lecturers/registerLecturer.sql', 'r') as file:
            sql_script = file.read()
            with app.app_context():
                db.session.execute(text(sql_script), {"account_id": user[0]})
                db.session.commit()
        return jsonify({"message": "Lecturer successfully registered"},{"username": username}), 201
    elif(account_type == 3):
        #register student
        with open('./app/sql/students/registerStudent.sql', 'r') as file:
            sql_script = file.read()
            with app.app_context():
                db.session.execute(text(sql_script), {"account_id": user[0]})
                db.session.commit()
        return jsonify({"message": "Student successfully registered"},{"username":username}), 201
    else:
        return INVALID_REGISTRATION
# ...