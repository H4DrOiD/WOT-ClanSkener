from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class RegisterForm(FlaskForm):
    nickname = StringField('Prezývka', validators=[DataRequired(), Length(min=3, max=50)])
    clan_name = StringField('Názov klanu', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Heslo', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Registrovať')

class LoginForm(FlaskForm):
    nickname = StringField('Prezývka', validators=[DataRequired()])
    password = PasswordField('Heslo', validators=[DataRequired()])
    submit = SubmitField('Prihlásiť sa')
