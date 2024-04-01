from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, number_range

class CreateUnitForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Create')

class EditUnitForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Update')

