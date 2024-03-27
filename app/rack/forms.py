from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, number_range
class CreateRackForm(FlaskForm):
    name = StringField('Rack name', validators=[DataRequired()])
    numberOfUnits = IntegerField('Number of Units', validators=[DataRequired(), number_range(1, 42)], default=1)
    active = BooleanField('Active', default=True)
    submit = SubmitField('Create')

class EditRackForm(FlaskForm):
    name = StringField('Rackname', validators=[DataRequired()])
    active = BooleanField('Active')
    submit = SubmitField('Edit')
    cancel = SubmitField('Cancel')
