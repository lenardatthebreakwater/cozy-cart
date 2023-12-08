from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, Email
from .models import User

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField("Confirm Password", validators=[EqualTo("password")])
    country = StringField("Country", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    contact = StringField("Contact", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    zipcode = StringField("Zip Code", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username is already taken")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email is already taken")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
