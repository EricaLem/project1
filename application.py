import os

from flask import Flask, session, render_template, request
from flask_session import Session # store session server-side
from sqlalchemy import create_engine, Column, Text, Integer, String, text
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_debugtoolbar import DebugToolbarExtension

#from models import *

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

DATABASE_URL = 'postgres://hszbrtnoxysrwz:f1e4c793c56b123ceb088f2f1175a64d84ce58efc4acc04bbec1d328908fce2e@ec2-34-193-42-173.compute-1.amazonaws.com:5432/d9n3d36eha0ujd'

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)  # Session created so the user's info can be maintained

# Set up database
#engine = create_engine(os.getenv("DATABASE_URL"))
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine)) # sessions for each user

reviews = []

# Routes

@app.route("/")			
def index():			
	return render_template("index.html")

@app.route("/signup")			
def signup():	
	"""Register for website"""		
	return render_template("signup.html")

@app.route("/login")			
def login():
	"""Login to website"""
	return render_template("login.html")

@app.route("/hello", methods=["POST"])			
def hello():
	username = request.form.get("username")
	password = request.form.get("password")

	# IF username exists
	if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount > 0:
		return render_template("error.html", message="Username already taken.")
 
	# OTHERWISE: insert into user table
	db.execute("INSERT INTO users (username, password) \
		VALUES (:username, :password)", {"username": username, "password": password}) 

	print(f"Now {username} is registered.")
	db.commit()
	return render_template("hello.html", name=username)

@app.route("/member", methods=["GET", "POST"])			
def member():
	"""Search for a book"""
	name = request.form.get("username")	
	user_ID = request.form.get("id")
	session["user_id"] = user_ID
	session["user_name"] = name

	allBooks = db.execute("SELECT * FROM books LIMIT 200").fetchall()
	return render_template("member.html", name=session["user_name"], allBooks=allBooks)

@app.route("/member/search", methods=["GET", "POST"])			
def search():
	"""Retrieve responses from search"""
	if request.method == "POST":
		book_id = request.form.get("book_id")

		book_id1 = '%' + book_id + '%'
		book_id2 = db.execute("SELECT * FROM books WHERE author LIKE :author \
								OR title LIKE :title", {"author": book_id1,"title": book_id1}).fetchall()

		return render_template("search.html", name=session["user_name"], book_id2=book_id2)


@app.route("/member/search/details", methods=["POST"])			
def details():
	# if request.method == "POST":
		result_id = request.form.get("result_id")
		result = db.execute("SELECT * FROM books WHERE id = :id", {"id": result_id}).fetchone()
		session["result"] = result
		rating = request.form.get("rating")
		review = request.form.get("review")
		print(f"RATING IS: {rating}.")

		if rating is not None:
			print("Review appended to list.")
			reviews.append(review)
			return render_template("details.html", result=result, reviews=reviews)

		else:
			return render_template("details.html", result=result, reviews=reviews)
			
	# if request.method == "GET":
	# 	result = session["result"]
	# 	return render_template("details.html", result=result, reviews=reviews)





if __name__ == "__main__":
	with app.app_context():
		main()

	# try:
	# 	result_id = int(request.form.get("result_id"))
	# except ValueError:
	# 	render_template("error.html", message="Sorry, we do not have a book matching that information... yet.")


	# author = request.form.get("author")	
	# isbn = request.form.get("isbn")	
	# year = request.form.get("year")	


	# userID = db.execute("SELECT id FROM users WHERE username = thing").fetchall()
	# session['user_id'] = userID
	# print(f"Now the Session ID is {userID}.")

# @app.route("/<string:name>", methods=["POST"])
# def account(name):	
# 	username = request.form.get("username")	
# 	user_ID = request.form.get("id")
# 	#session['user_id'] = user_ID
# 	return f"Hiya, {name}!"

	# # Query for the book
	# if db.execute("SELECT * FROM books WHERE author = :author", {"author": book_id}).rowcount > 0:
	# 	#return render_template("success.html", name=session["user_name"], message="We have books by that author.")
	# 	return render_template("search.html", name=session["user_name"], book_id=book_id)

	# elif db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": book_id}).rowcount > 0:
	# 	return render_template("success.html", name=session["user_name"], message="We have that book.")

	# elif db.execute("SELECT * FROM books WHERE title = :title", {"title": book_id}).rowcount > 0:
	# 	return render_template("success.html", name=session["user_name"], message="We have that title.")

	# # db.execute("SELECT author FROM books WHERE author = :author", {"author": book_id})
	# return render_template("error.html", message="Sorry, we do not have a book matching that information... yet.")