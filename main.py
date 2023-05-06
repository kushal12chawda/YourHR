from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from flask_marshmallow import Marshmallow

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'kushalisasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'applications.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    email = db.Column(db.String(150))

class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    phone = db.Column(db.Integer)
    job = db.Column(db.String(150))
    city = db.Column(db.String(150))
    filename = db.Column(db.String(150))
    file = db.Column(db.LargeBinary)

with app.app_context():
    db.create_all()    

# Define the home page route
@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/signup_post', methods=['GET', 'POST'])
def signup_post():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        new_entry = Login(username = username, password = password, email = email)
        db.session.add(new_entry)
        db.session.commit()
        # return redirect(url_for('post_details'))
        return redirect(url_for("post_details", name = username))
    return render_template('signup.html')

@app.route('/post_details/<name>', methods=['GET', 'POST'])
def post_details(name):
    if request.method == 'POST':
        file = request.files['file']
        f_name = request.form.get("firstname")
        l_name = request.form.get("lastname")
        phone = request.form.get("phone")
        job = request.form.get("job")
        city = request.form.get("city")
        new_entry = Applicant(first_name = f_name, last_name = l_name, phone = phone, job = job, city = city, filename = file.filename, file=file.read())
        db.session.add(new_entry)
        db.session.commit()
        flash("Application Submitted Successfully !!")
        return redirect(url_for('post_details', name = name))
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)