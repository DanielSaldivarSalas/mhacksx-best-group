from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DecimalField, FloatField
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(min=4, max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    pic_url = StringField('pic_url')


class BuySellBitcoin(FlaskForm):
    'bitcoin/sell and bitcoin/buy'
    amount = FloatField('amount', validators=[InputRequired()])
