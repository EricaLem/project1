import os
import requests # for access to GoodReads API

from flask import Flask, session, render_template, request, jsonify
from flask_session import Session # store session server-side
from sqlalchemy import create_engine, Column, Text, Integer, String, text
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

DATABASE_URL = 'postgres://hszbrtnoxysrwz:f1e4c793c56b123ceb088f2f1175a64d84ce58efc4acc04bbec1d328908fce2e@ec2-34-193-42-173.compute-1.amazonaws.com:5432/d9n3d36eha0ujd'

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# the toolbar is only enabled in debug mode:
app.debug = True # disable when done
app.config["SECRET_KEY"] = "enableCookies" # set a 'SECRET_KEY' to enable the Flask session cookies
toolbar = DebugToolbarExtension(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)  # Session created so the user's info can be maintained

GoodReadsAPIKey = "EApqSumsCZMIrnDlflgQ" 
# Set up database
#engine = create_engine(os.getenv("DATABASE_URL"))
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine)) # sessions for each user

reviews = []

# Routes

@app.route("/")			
def index():	
	# SECRET KEYS
	session["username"] = "admin"
	session["user_ID"] = 0	
	# session["reviews"] = []	
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
	if request.method == "POST":
		session.pop("username", None)
		session.pop("user_ID", None)
		usrname = request.form.get("username")
		user = db.execute("SELECT * FROM users WHERE username = :username", {"username": usrname}).fetchone()
		print(f"USER: {user}.")
		session["username"] = user.username
		session["user_ID"] = user.id
		print(f'USER: {session["username"]}.')

		allBooks = db.execute("SELECT * FROM books LIMIT 1000").fetchall()
		return render_template("member.html", name=session["username"], allBooks=allBooks)

@app.route("/member/search", methods=["GET", "POST"])			
def search():
	print(f'FROM SEARCH, USER: {session["username"]}.')
	"""Retrieve responses from search"""
	if request.method == "POST":
		book_id = request.form.get("book_id")

		book_id1 = '%' + book_id + '%'
		book_id2 = db.execute("SELECT * FROM books WHERE author LIKE :author \
								OR title LIKE :title OR isbn LIKE :isbn", \
								{"author": book_id1,"title": book_id1,"isbn": book_id1}).fetchall()

		return render_template("search.html", name=session["username"], book_id2=book_id2)


@app.route("/member/search/details", methods=["POST"])			
def details():
	result_id = request.form.get("result_id")
	rating = request.form.get("rating")
	review = request.form.get("review")
	ratingsGR = [100,100]

	session["old_reviews"] = db.execute("SELECT * FROM reviews WHERE book_id = :id", {"id": result_id}).fetchall()

	if result_id is not None:
		result = db.execute("SELECT * FROM books WHERE id = :id", {"id": result_id}).fetchone()
		session["result"] = result
		session["result_id"] = result.id
		isbntest = session["result"].isbn
		#isbntest = "9781632168146"

		# Request API key from GoodReads
		# 9781632168146
		res = requests.get("https://www.goodreads.com/book/review_counts.json", \
				params={"key": GoodReadsAPIKey, "isbns": isbntest})

		if res.status_code != 200:
		 	# raise Exception("ERROR: API request unsuccessful.")
		 	return render_template("details.html", result=session["result"], reviews=session["old_reviews"], rating=ratingGR)

		data = res.json()
		print(data)
		session["rating_avg"] = data['books'][0]['average_rating']
		session["rating_number"] = data['books'][0]['work_ratings_count']
		ratingGR = [session["rating_avg"], session["rating_number"]]
					
		return render_template("details.html", result=session["result"], reviews=session["old_reviews"], rating=ratingGR)

	if rating is not None:
		print("Review appended to list.")
		# INSERT into review table
		db.execute("INSERT INTO reviews (rating, submission, book_id, user_id, username) \
		 			VALUES (:rating, :submission, :book_id, :user_id, :username)", \
		 			{"rating":rating, "submission":review, "book_id":session["result_id"], \
		 			"user_id":session["user_ID"], "username":session["username"]})
		# if statement >> if user has review_id == MAX(reviews.id) - 1
		#	DO NOT ADD

		reviews.append(review)
		db.commit()
		session["old_reviews"] = db.execute("SELECT * FROM reviews WHERE book_id = :id", {"id": session["result_id"]}).fetchall()
		return render_template("details.html", result=session["result"], reviews=session["old_reviews"], rating=ratingGR)

	else:
		return render_template("details.html", result=session["result"], reviews=session["old_reviews"], rating=ratingGR)
			
	# if request.method == "GET":
	# 	result = session["result"]
	# 	return render_template("details.html", result=result, reviews=reviews)


# OTHERWISE: insert into review table
	# db.execute("INSERT INTO reviews (rating, submission, book_id, user_id) \
	# 	VALUES (:rating, :submission, :book_id, :user_id)", \
	# 	{"rating":rating, "submission":submission, "book_id":book_id, "user_id":user_id}) 


if __name__ == "__main__":
	with app.app_context():
		main()

		# print(f"RATING IS: {rating}.")
		# print(f"REVIEW IS: {review}.")
		# print(f'FROM DETAILS, USER: {session["username"]}.')
		# print(f'FROM DETAILS, BOOK_ID: {session["result_id"]}.')

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