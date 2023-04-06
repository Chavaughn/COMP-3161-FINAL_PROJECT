from flask import request
from app.controllers.AppController import *

# === Register functionality ===

@app.route('/register', methods=['POST', 'GET'])
def register_postman():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    password = request.json['password']
    email = request.json['email']
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
    if (account_type == 2):
        #register lecturer
        print(f"___________________________________{username}: Lecturer{first_name} {last_name}_____________________________")
    elif(account_type == 3):
        #register student
        print(f"___________________________________{username}: Student{first_name} {last_name}_____________________________")
    else:
        return redirect(url_for('landing'))
    return redirect(url_for('landing'))
    

# ...