import csv
import random
from sqlalchemy import create_engine, text
from app import app, db
from werkzeug.security import generate_password_hash

print("____________Creating the database____________")
with app.app_context():
    #Edit this line to match your password
    engine = create_engine('mysql+pymysql://root:NilArie12@localhost:3306')
    with open('./app/sql/create_db.sql', 'r') as file:
        sql_script = file.read()
        with engine.connect() as conn:
            conn.execute(text(sql_script))
print("____________Database Created____________")
print("____________Adding Tables____________")
with open('./app/sql/create_tables.sql', 'r') as file:
    sql_script = file.read()
    with app.app_context():
        db.session.execute(text(sql_script))
        db.session.commit()
print("____________Tables Added____________")
print("____________Populating Tables____________")
with open('./app/res/firstnames.txt') as f1, open('./app/res/lastnames.txt') as f2:
    first_names = f1.read().splitlines()
    last_names = f2.read().splitlines()

accounts = []
counter = 0
password = generate_password_hash("password", method='pbkdf2:sha256')
for first_name in first_names:
    for last_name in last_names:
        username = 6201420000+counter
        email = f"{username}@mymona.uwi.edu"
        account_type = 3
        accounts.append({
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "password": password,
            "email": email,
            "account_type": account_type
        })
        full_name = f"{first_name} {last_name}"
        counter = counter+1
with open('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/accounts.csv', 'w', newline='') as csvfile:
    fieldnames = ['first_name', 'last_name', 'username','password', 'email', 'account_type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for account in accounts:
        writer.writerow(account)

with open('./app/sql/initialize_accounts.sql', 'r') as file:
    sql_script = file.read()
    with app.app_context():
        db.session.execute(text(sql_script))
        db.session.commit()

from app import enrolment_data

with open('./app/sql/initialize_enrollments.sql', 'r') as file:
    sql_script = file.read()
    with app.app_context():
        db.session.execute(text(sql_script))
        db.session.commit()


print("____________Tables Populated____________")
