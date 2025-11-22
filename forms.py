from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class MessageForm(FlaskForm):
    body = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")
