from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    name = StringField(
        label="Name:",
        validators=[DataRequired(message="This field is required")])
    username = StringField(
        label="Login:",
        validators=[DataRequired(message="This field is required")])
    password = PasswordField(
        label="Password",
        validators=[DataRequired(message="This field is required"),
                    Length(min=5, message="Password must be at least 5 characters long")])


class LoginForm(FlaskForm):
    username = StringField(
        label="Login:",
        validators=[DataRequired(message="This field is required")])
    password = PasswordField(
        label="Password",
        validators=[DataRequired(message="This field is required")])
