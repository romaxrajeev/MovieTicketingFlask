from OSTL import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from OSTL.routes import *


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f"User('{ self.name }','{ self.email }')"

class Movies(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	email = db.Column(db.String(120), nullable=False)
	moviename = db.Column(db.String(50),nullable=False)
	moviedate = db.Column(db.String(20),nullable=False)
	movietime = db.Column(db.String(20),nullable=False)
	movietheatre = db.Column(db.String(150),nullable=False)
	movieseat = db.Column(db.String(200),nullable=False)
	eatable = db.Column(db.String(200),nullable=False)

	def __repr__(self):
		return f"('{self.moviename}','{self.moviedate}','{self.movietime}','{self.movietheatre}','{self.movieseat}','{self.eatable}')"
