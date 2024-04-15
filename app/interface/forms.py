from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired


class CreateInterfaceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    type = SelectField('Type', choices=[('USB', 'USB'), ('Ethernet', 'Ethernet'), ('Serial', 'Serial'),
                                        ('VGA', 'VGA'), ('HDMI', 'HDMI'), ('Serial', 'Serial'),
                                        ('Parallel', 'Parallel'), ('SD / Micro SD', 'SD / Micro SD'),
                                        ('SFP', 'SFP'), ('Power', 'Power'), ('Wireless', 'Wireless'),('Other', 'Other')])
    hardware = SelectField('Hardware', coerce=int, choices=(), validators=[DataRequired()])
    active = BooleanField('Active', default=True)
    submit = SubmitField('Create')

class EditInterfaceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    type = SelectField('Type', choices=[('USB', 'USB'), ('Ethernet', 'Ethernet'), ('Serial', 'Serial'),
                                        ('VGA', 'VGA'), ('HDMI', 'HDMI'), ('Serial', 'Serial'),
                                        ('Parallel', 'Parallel'), ('SD / Micro SD', 'SD / Micro SD'),
                                        ('SFP', 'SFP'), ('Power', 'Power'), ('Wireless', 'Wireless'),('Other', 'Other')])
    hardware = SelectField('Hardware', coerce=int, choices=(), validators=[DataRequired()])
    active = BooleanField('Active', default=True)
    submit = SubmitField('Edit')
    supress = SubmitField('Cancel')

