import csv 
import os 

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL")) 
#// create a db engine; an object created by sqlalchemy which will manage connections to db
db = scoped_session(sessionmaker(bind = engine))
#// db is the variable that will allow us to run SQL commands

def main():
	f = open("books.csv")
	# # reader() is a built-in Python module specifically for CSV files
	reader = csv.reader(f)
	for isbn, title, author, year in reader:
	# 	# :origin is sqlalchemy placeholder
	# 	# db.execute executes an INSERTION
		db.execute ( "INSERT INTO books (isbn, title, author, year) \
	 		VALUES (:isbn, :title, :author, :year)", \
	 		{ "isbn":isbn, "title":title, "author":author, "year":year })
	print("Successfully added books from books.csv to database.");
	# save changes (SQLAlchemy)
	db.commit()		# db.commit() saves the changes i just made (SINCE UPDATING THINGS)

if __name__ == "__main__":
	main()
