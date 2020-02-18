# models.py

#import os

#from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# one class = one table in SQL database
# db.Model communicates with the flask-SQLalchemy library

# Class 1. Flight
class Book(db.Model):
	__tablename__ = "books"
	id = db.Column( db.Integer, primary_key=True )
	isbn = db.Column( db.String, nullable=False )
	title = db.Column( db.String, nullable=False )
	author = db.Column( db.String, nullable=False )
	year = db.Column( db.Integer, nullable=False )

	def add_passenger(self, name):
		p = Passenger(name=name, flight_id=self.id)
		db.session.add(p)
		db.session.commit()

# Class 2. User
class User(db.Model):
	__tablename__ = "users"
	id = db.Column( db.Integer, primary_key=True )
	username = db.Column( db.String, nullable=False )
	password = db.Column( db.String, nullable=False )

# Class 3. Reviews
class Review(db.Model):
	__tablename__ = "reviews"
	id = db.Column( db.Integer, primary_key=True )
	name = db.Column( db.String, nullable=False )
	# user_id = FOREIGN KEY - references ID column of users table
	user_id = db.Column( db.Integer, db.ForeignKey("users.id"), nullable=False )