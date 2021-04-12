from forms import CreatePlaceForm, Registration, Login

import datetime as dt
from functools import wraps
import os

from osm import MapQuery

from flask import Flask, render_template, redirect, url_for, request, flash
from flask import abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
ckeditor = CKEditor(app)
Bootstrap(app)
GoogleMaps(app)

year = dt.datetime.now().year
app.config['SECRET_KEY'] = "123"
# os.environ.get('SECRET_KEY')

## CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL",  "sqlite:///bookshops.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['GOOGLEMAPS_KEY'] = "AIzaSyA0ZfOh9dwpZXB3r5RoiA8_ZA7fUYM5Nq0"
db = SQLAlchemy(app)

# LOGIN PERMISSIONS SETUP
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

## CONFIGURE TABLES
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password =db.Column(db.String(), nullable=False)

class PlacePost(db.Model):
    __tablename__ = "place_posts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(), nullable=False)
    website = db.Column(db.String(), nullable=False)
    lat = db.Column(db.Float(), nullable=False)
    lon = db.Column(db.Float(), nullable=False)
    vibe = db.Column(db.Text(), nullable=False)

# db.create_all()

## ADD OSM DATA TO DATABASE
# key = "amenity"
# value = "library"
# location = "3605396194"
#
# osm = MapQuery()
# data = osm.query(key, value, location)
# data_series = osm.series (data, value)
#
# for i in range (0,len (data_series[0])):
#     db.session.add(PlacePost(name=data_series[0][i], type=data_series[1][i], website =data_series[2][i], lat=data_series[3][i], lon=data_series[4][i], vibe="Register to add!"))
#     db.session.commit()
    # print (f"***{data_series[0][i]}, {data_series[1][i]}, {data_series[2][i]}, {data_series[3][i]}***")

## ROUTES
@app.route('/')
def home():
    place_data = PlacePost.query.all()
    return render_template("index.html", places=place_data, year = year, logged_in=current_user.is_authenticated)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Registration()
    if form.validate_on_submit():
        if User.query.filter_by(email=request.form['email']).first():
            flash("The email address you have provided already exists in the Bibliophile database. Please login.")
            return redirect(url_for('login'))
        else:
            new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=generate_password_hash(request.form["password"], method='pbkdf2:sha256', salt_length=8)
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))
    return render_template("register.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form=Login()
    if request.method == 'POST':
        password = request.form["password"]
        email = request.form["email"]
        user = User.query.filter_by(email=email).first()
        if not user:
            flash ("That email does not exist, please try again.")
            return redirect (url_for ('login'))
        elif not check_password_hash(user.password, password):
            flash ("Password not correct, please try again.")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/add_place', methods=['GET', 'POST'])
def new_post():
    form = CreatePlaceForm()
    if form.validate_on_submit():
        new_post = PlacePost(
        name = form.name.data,
        type = form.type.data,
        website = form.website.data,
        lat = form.lat.data,
        lon = form.lon.data,
        vibe = form.vibe.data
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("create_post.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/edit_post/<int:num>', methods=['GET', 'POST'])
def edit_post(num):
    place = db.session.query(PlacePost).filter_by(id=num).first()
    edit_form = CreatePlaceForm(
        name=place.name,
        type=place.type,
        website=place.website,
        lat=place.lat,
        lon=place.lon,
        vibe=place.vibe
    )
    if edit_form.validate_on_submit():
        place.name = edit_form.name.data
        place.type = edit_form.type.data
        place.website = edit_form.website.data
        place.lat = edit_form.lat.data
        place.lon = edit_form.lon.data
        place.vibe = edit_form.vibe.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit_post.html", form=edit_form, is_edit=True, num=num, logged_in=current_user.is_authenticated)

@app.route('/delete_post/<int:num>', methods=['GET', 'POST'])
def delete_post(num):
    place = db.session.query(PlacePost).filter_by(id=num).first()
    db.session.delete(place)
    db.session.commit()
    return redirect(url_for('home'))


## RUN APP

if __name__ == "__main__":
    app.run(debug=True)





