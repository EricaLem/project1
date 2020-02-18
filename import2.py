import csv 
import os 

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = 'postgres://hszbrtnoxysrwz:f1e4c793c56b123ceb088f2f1175a64d84ce58efc4acc04bbec1d328908fce2e@ec2-34-193-42-173.compute-1.amazonaws.com:5432/d9n3d36eha0ujd'

#engine = create_engine(os.getenv("DATABASE_URL")) 
engine = create_engine(DATABASE_URL)
#// create a db engine; an object created by sqlalchemy which will manage connections to db
db = scoped_session(sessionmaker(bind = engine))
#// db is the variable that will allow us to run SQL commands
db.SQLALCHEMY_DATABASE_URI = DATABASE_URL

def main():

	book = db.execute("SELECT * FROM books LIMIT 1").fetchall()

	print(book)
	print(book[0][2])

	u = "Erica Lemieux"
	p = "Bobmarley1!"
	db.execute ("INSERT INTO users (username, password) VALUES ('%(username)s', '%(password)s')" %{'username': u, 'password': p}) 
	db.commit()
	print(f"Added {u} to database.")

	# "INSERT INTO users (username, password) VALUES 
	# ('%(username)s', '%(password)s')" %{'username': u, 'password': p}


	# f = open("books.csv")
	# reader = csv.reader(f)
	# for isbn, title, author, year in reader:
	# 	# :origin is sqlalchemy placeholder
	# 	# db.execute executes an INSERTION
	#  	db.execute ( "INSERT INTO books (isbn, title, author, year) \
	#  		VALUES (:isbn, :title, :author, :year)", \
	#  		{ "isbn":isbn, "title":title, "author":author, "year":year })
	# isbn = "098340fgsdfs9df80"
	# title = "100 Years of Solitude"
	# author = "Gabriel Garcia Marquez"
	# year = 1959
	# db.execute ( "INSERT INTO books (isbn, title, author, year) \
	#  		VALUES (:isbn, :title, :author, :year)", \
	#  		{ "isbn":isbn, "title":title, "author":author, "year":year })
	# print("Successfully addedGabriel Garcia to database.");
	# #print("Successfully added books from books.csv to database.");
	# # save changes (SQLAlchemy)
	# db.commit()		# db.execute saves the changes i just made (SINCE UPDATING THINGS)



if __name__ == "__main__":
	main()


	# username = "Erica Lemieux"
	# password = "Bobmarley1!"
	# db.execute ("INSERT INTO users (username, password) VALUES (:username, :password)", { "username": username, "password": password }) 
	# print(f"Added {username} to database.");