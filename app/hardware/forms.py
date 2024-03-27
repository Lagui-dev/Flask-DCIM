from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired


class CreateHardwareForm(FlaskForm):
    name = StringField('Hardware Name', validators=[DataRequired()])
    type = SelectField('Type', choices=[('', ''), ('CPU', 'CPU'), ('GPU', 'GPU'), ('RAM', 'RAM'), ('Storage', 'Storage')])
    active = BooleanField('Active', default=True)
    submit = SubmitField('Create')

class EditHardwareForm(FlaskForm):
    name = StringField('Hardware Name', validators=[DataRequired()])
    type = SelectField('Type', choices=[('', ''), ('CPU', 'CPU'), ('GPU', 'GPU'), ('RAM', 'RAM'), ('Storage', 'Storage')])
    active = BooleanField('Active', default=True)
    submit = SubmitField('Edit')
    supress = SubmitField('Cancel')

