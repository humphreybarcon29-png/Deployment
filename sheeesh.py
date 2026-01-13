from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'BARCON')

DB_USER = os.environ.get('MYSQLUSER', 'root')
DB_PASSWORD = os.environ.get('MYSQLPASSWORD', '')
DB_HOST = os.environ.get('MYSQLHOST', 'localhost')
DB_PORT = os.environ.get('MYSQLPORT', '3306')
DB_NAME = os.environ.get('MYSQLDATABASE', 'chapter_renewal')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'input'
    id = db.Column(db.Integer, primary_key=True)
    Chapter_of_Origin = db.Column(db.String(100), nullable=False)
    Chapter_Company = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/renewal', methods=['POST'])
def renewal():
    CO = request.form.get('CO')
    CC = request.form.get('CC')
    AIN = request.form.get('AIN')
    PS = request.form.get('PS')
    if not all([CO, CC, AIN, PS]):
        return "All fields required!", 400
    user = User(Chapter_of_Origin=CO, Chapter_Company=CC, email=AIN, password=PS)
    db.session.add(user)
    db.session.commit()
    return "Success!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
