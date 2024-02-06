from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class NewUser(FlaskForm):
    user_name = StringField('Name', validators=[DataRequired()])
    user_password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class CurrentUser(FlaskForm):
    user_name = StringField('Name', validators=[DataRequired()])
    user_password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AddProduct(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Add')