from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class NameSearchForm(FlaskForm):
    name = StringField("Enter your Name", validators=[DataRequired()])
    #sem_no = StringField("Enter semester number", validators=[DataRequired()])
    #sem_no = StringField("Enter semester number")
    submit = SubmitField('Search database for results')

class ConfirmName(FlaskForm):
    item_no = StringField("Enter the number of the result you are interested in", validators=[DataRequired()])
    submit = SubmitField('Display results')

class RankCheckerForm(FlaskForm):
    sem_no = StringField("Enter semester number(or 10 for cumulative) ", validators=[DataRequired()])
    gpa = StringField("Enter gpa ", validators=[DataRequired()])
    submit = SubmitField('Display results')

class AnalyserForm(FlaskForm):
    sem_no = StringField("Enter semester number(or 10 for cumulative) ", validators=[DataRequired()])
    #gpa = StringField("Enter gpa ", validators=[DataRequired()])
    submit = SubmitField('Display results')
