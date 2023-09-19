from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, TimeField
from wtforms.validators import InputRequired, EqualTo

class Loginform(FlaskForm):
    user_id = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Login")

class Registrationform(FlaskForm):
    user_id = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    password2 = PasswordField("Confirm Password:", 
        validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Register")

class Eventform(FlaskForm):
    title = StringField("Title:", validators=[InputRequired()])
    details = StringField("Details:", validators=[InputRequired()])
    submit = SubmitField("Submit")

class Dateform(FlaskForm):
    event_date = DateField("Event Date:", validators=[InputRequired()])
    event_start = TimeField("From:", validators=[InputRequired()])
    event_end = TimeField("To:", validators=[InputRequired()])
    details = StringField("Details:")
    submit = SubmitField("Create event")

class Editform(FlaskForm):
    event_date = DateField("Event Date:", validators=[InputRequired()])
    event_start = TimeField("From:", validators=[InputRequired()])
    event_end = TimeField("To:", validators=[InputRequired()])
    details = StringField("Details:")
    submit = SubmitField("Edit event")
