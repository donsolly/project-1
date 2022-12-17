import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://eeiozxjcrbiepu:81084a7df040d3e3d3589cc172561bc1ca5dd9f35a994de475eee464fa344683@ec2-18-210-214-86.compute-1.amazonaws.com:5432/d4ckpntkc1m45d")
db = scoped_session(sessionmaker(bind=engine))

def main():
    db.execute("CREATE TABLE books(id SERIAL PRIMARY KEY, isbn VARCHAR NOT NULL , title VARCHAR NOT NULL, author VARCHAR NOT NULL, year VARCHAR NOT NULL)")
    db.execute("CREATE TABLE users(id SERIAL PRIMARY KEY , username VARCHAR NOT NULL, password VARCHAR NOT NULL)")
    db.execute("CREATE TABLE ratings(isbn VARCHAR NOT NULL , review VARCHAR NOT NULL, rating INTEGER NOT NULL, username VARCHAR NOT NULL)")
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:

        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",{"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added books from {author} with isbn: {isbn} and title: {title} published on {year}.")
    db.commit()

if __name__ == "__main__":
    main()

#See lecture for new import or 39:46mins to do it.