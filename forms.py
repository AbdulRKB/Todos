from flask_wtf import FlaskForm, CSRFProtect
from wtforms import SubmitField

class submitIt(FlaskForm):
	submit = SubmitField("Submit")