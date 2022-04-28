from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length

# You can add the features specific to particular type of forms (SignUp / Login)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(min=3)])
    pwd = StringField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(min=3)])
    pwd = StringField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('SignUp')
