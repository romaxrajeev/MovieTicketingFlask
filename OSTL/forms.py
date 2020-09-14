from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from OSTL.models import User
from OSTL.routes import *

class RegistrationForm(FlaskForm):
	name = StringField('Name',validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email',validators=[DataRequired(), Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
	signup_btn = SubmitField('Sign Up')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email already exists.')


class LoginForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	login_btn = SubmitField('Login')


class MovieForm(FlaskForm):
	movie_date = SelectField('Date',choices=[('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),])
	movie_theatre = SelectField('Theatre',choices=[('Inox','INOX'),('PVR','PVR'),('Cinemax','Cinemax')])
	seat_class = StringField('Seat Class',validators=[DataRequired()])
	meal = SelectField('Meal',choices=[('Pizza and Coke','Pizza and Coke'),('Burger and Coke','Burger and Coke'),('Popcorn','Popcorn'),('Waffles','Waffles')])
	book = SubmitField('Book my ticket')
