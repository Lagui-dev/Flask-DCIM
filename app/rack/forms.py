from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, number_range
class CreateRackForm(FlaskForm):
    name = StringField('Rackname', validators=[DataRequired()])
    numberOfUnits = IntegerField('Number of Units', validators=[DataRequired(), number_range(1, 42)], default=1)
    active = BooleanField('Active', default=True)
    submit = SubmitField('Add')

class EditRackForm(FlaskForm):
    name = StringField('Rackname', validators=[DataRequired()])
    active = BooleanField('Active')
    submit = SubmitField('Update')
    cancel = SubmitField('Cancel')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class DeleteRackForm(FlaskForm):
    submit = SubmitField('Delete')

class readRackForm(FlaskForm):
    name = StringField('Rackname', validators=[DataRequired()])
    active = BooleanField('Active', default=True)
    def __init__(self, name, active):
        super(readRackForm, self).__init__(*args, **kwargs)
        read_only(self.name)