from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, URL

class CreatePlaceForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    type = StringField("Type (library, books (shop), cafe, etc.)", validators=[DataRequired()])
    website = StringField("URL")
    lat = FloatField("Map Coordinates (latitude)")
    lon = FloatField("Map Coordinates (longitude)")
    vibe = StringField("Vibe - What's it like? Who's there? What's everyone doing?")
    submit = SubmitField("Submit Post")

class Registration(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password =PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class Login(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

