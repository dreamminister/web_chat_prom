from wtforms.validators import DataRequired
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length, Regexp
from wtforms import ValidationError
from ..models import Room


class AddRoomForm(Form):
    name = StringField('Name', validators=[
    DataRequired(), Length(1, 32), Regexp('^[A-Za-z][A-Za-z0-9]*$', 0,
    "Room's name must have only letters or numbers")])

    description = TextAreaField('Description', validators=[DataRequired(), Length(1, 300)])
    submit = SubmitField('Add room')

    def validate_name(self, field):
        if Room.query.filter_by(name=field.data).first():
            raise ValidationError("Room's name already in use.")