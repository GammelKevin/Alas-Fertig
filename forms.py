from flask_wtf import FlaskForm
from wtforms import StringField, TimeField, BooleanField, DateField
from wtforms.validators import DataRequired

class OpeningHoursForm(FlaskForm):
    pass  # Wir verwenden nur das CSRF-Token aus dem FlaskForm
