import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 'BARCON'

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.environ['MYSQLUSER']}:"
    f"{os.environ['MYSQLPASSWORD']}@"
    f"{os.environ['MYSQLHOST']}:"
    f"{os.environ['MYSQLPORT']}/"
    f"{os.environ['MYSQLDATABASE']}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    Chapter_of_Origin = db.Column(db.String(100), nullable=False)
    Chapter_Company = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

@app.route('/')
def home():
    return render_template('renewal.html')

@app.route('/renewal', methods=['POST'])
def renewal():
    CO = request.form.get('CO')
    CC = request.form.get('CC')
    AIN = request.form.get('AIN')
    PS = request.form.get('PS')

    if not all([CO, CC, AIN, PS]):
        flash('All fields required!', 'error')
        return redirect(url_for('home'))

    if User.query.filter_by(email=AIN).first():
        flash('Email already registered!', 'error')
        return redirect(url_for('home'))

    try:
        hashed_password = generate_password_hash(PS)
        user = User(
            Chapter_of_Origin=CO,
            Chapter_Company=CC,
            email=AIN,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Success!', 'success')
    except Exception:
        db.session.rollback()
        flash('Database error!', 'error')

    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
