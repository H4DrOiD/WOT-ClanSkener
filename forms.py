from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length

class RegistrationForm(FlaskForm):
    nickname = StringField("Prezývka", validators=[DataRequired(), Length(min=2, max=100)])
    clan_name = StringField("Názov klanu", validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField("Heslo", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Potvrď heslo", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Registrovať")

class LoginForm(FlaskForm):
    nickname = StringField("Prezývka", validators=[DataRequired()])
    password = PasswordField("Heslo", validators=[DataRequired()])
    submit = SubmitField("Prihlásiť sa")
