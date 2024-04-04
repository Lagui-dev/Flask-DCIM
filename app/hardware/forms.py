from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired


class CreateHardwareForm(FlaskForm):
    name = StringField('Hardware Name', validators=[DataRequired()])
    type = SelectField('Type', choices=[('', ''), ('Server', 'Server'), ('Switch', 'Switch'), ('Router', 'Router'), ('SAN/NAS', 'SAN/NAS'),
                                        ('Firewall', 'Firewall'), ('Accessories', 'Accessories'), ('Patch Panel', 'Patch Panel'),
                                        ('Other', 'Other')])
    active = BooleanField('Active', default=True)
    submit = SubmitField('Create')

class EditHardwareForm(FlaskForm):
    name = StringField('Hardware Name', validators=[DataRequired()])
    type = SelectField('Type', choices=[('', ''), ('Server', 'Server'), ('Switch', 'Switch'), ('Router', 'Router'), ('SAN/NAS', 'SAN/NAS'),
                                        ('Firewall', 'Firewall'), ('Accessories', 'Accessories'), ('Patch Panel', 'Patch Panel'),
                                        ('Other', 'Other')])
    active = BooleanField('Active', default=True)
    submit = SubmitField('Edit')
    supress = SubmitField('Cancel')

class LinkHardwareUnitForm(FlaskForm):
    rack = SelectField('Rack', coerce=int, choices=(), validators=[DataRequired()])
    unit = SelectField('Unit', coerce=int, choices=(), validate_choice=False)
    submit = SubmitField('Link')