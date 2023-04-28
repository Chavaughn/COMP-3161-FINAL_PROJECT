from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, FileField, SubmitField, DateField, EmailField, RadioField
from wtforms.validators import InputRequired, EqualTo, Email
from flask_wtf.file import FileAllowed, DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegistrationForm(FlaskForm):
    firstname = StringField('*First Name', validators=[DataRequired()])
    lastname = StringField('*Last Name', validators=[DataRequired()])
    password = PasswordField('*Password', validators=[DataRequired()])
    confirm_password = PasswordField('*Confirm Password', validators=[DataRequired(), EqualTo('password')])
    account_type =RadioField("Select account type", choices=[(3,"Student"),(2,"Lecturer")])

class RegisterForCourseForm(FlaskForm):
    course_code = SelectField('Course', validators=[DataRequired()])

class AddCourseForm(FlaskForm):
    course_code = StringField('Course code:', validators=[DataRequired()])
    course_title = StringField('Course Title:', validators=[DataRequired()])
    course_description = TextAreaField('Course Description', validators=[DataRequired()])
    # lecturer = SelectField('lecturer')

class CreateCalendarEventForm(FlaskForm):
    course_code =  SelectField('Course code:', validators=[DataRequired()])
    calendar_event_name = StringField('Event Name:', validators=[DataRequired()])
    due_date = DateField('Date Due', validators=[DataRequired()])

