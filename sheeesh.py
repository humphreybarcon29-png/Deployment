from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'BARCON')  

# Use Railway MySQL vars or fallback (for local dev)
DB_USER = os.environ.get('MYSQLUSER', 'root')
DB_PASSWORD = os.environ.get('MYSQLPASSWORD', '')
DB_HOST = os.environ.get('MYSQLHOST', 'localhost')
DB_PORT = os.environ.get('MYSQLPORT', '3306')
DB_NAME = os.environ.get('MYSQLDATABASE', 'chapter_renewal')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

class User(db.Model):
    __tablename__ = 'input'
    id = db.Column(db.Integer, primary_key=True)
    Chapter_of_Origin = db.Column(db.String(100), nullable=False)
    Chapter_Company = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

@app.route('/')
def home():
    return render_template('register.html')  

@app.route('/renewal', methods=['POST'])
def renewal():
    CO = request.form.get('CO')
    CC = request.form.get('CC')
    AIN = request.form.get('AIN')
    PASSWORD = request.form.get('PS')
    if not all([CO, CC, AIN, PASSWORD]):
        flash('All fields required!', 'error')
        return redirect(url_for('home'))
    existing_user = User.query.filter_by(email=AIN).first()
    if existing_user:
        flash('Email already registered!', 'error')
        return redirect(url_for('home'))

    new_user = User(
        Chapter_of_Origin=CO,
        Chapter_Company=CC,
        email=AIN,
        password=PASSWORD)
    try:
        db.session.add(new_user)
        db.session.commit()
        flash('Renewal successful!', 'success')
        return redirect(url_for('home'))  
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('home'))

@app.route('/success')
def success():
    return '<h1>Success!</h1>'  

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
