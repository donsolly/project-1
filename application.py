import os
import requests
import simplejson as json
from flask import Flask, session, render_template, request, jsonify, redirect, flash
from flask_session import Session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt
from decimal import Decimal

app = Flask(__name__)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.secret_key = 'some_secret' #flashmessage setup

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


#index page 
@app.route("/", methods=["GET","POST"])
def index():
   message = "Sign In"
   enter = "Enter"
   invalidinfo = "Invalid Username or Password"
   session['logged_in'] = False
   if request.method == "POST":
      username = request.form.get("username")
      password = request.form.get("password")
      userdata = db.execute("SELECT * FROM users WHERE username = :username",{"username": username})
      if userdata.rowcount == 0:
         return render_template('index.html', invalidinfo=invalidinfo, message=message, enter=enter)
      data = userdata.fetchone()[2]
      if sha256_crypt.verify(request.form['password'], data):
         session['logged_in'] = True
         session['storing'] = username
         return render_template('dashboard.html')
      else:
         return render_template('index.html', invalidinfo="invalidinfo", message=message, enter=enter)
   return render_template("index.html", message=message, enter=enter)

#Registration Page 
@app.route("/register", methods=["GET","POST"])
def register():
   message = "Register"
   enter = "Submit"
   inuse = "Username in Use"
   session['logged_in'] = False
   successlog = "Successful Registration"
   if request.method == "POST":
      username = request.form.get("username")
      password = request.form.get("password")
      secure_password=sha256_crypt.encrypt(str(password))
      if db.execute("SELECT * FROM users WHERE username = :username",{"username": username}).rowcount == 1:
         return render_template("index.html", inuse=inuse, message=message, enter=enter)
      db.execute("INSERT INTO users (username, password) VALUES (:username,:password)",{"username": username, "password": secure_password})
      db.commit()
      return render_template("index.html", sucesslog=successlog, message=message, enter=enter)
      session.clear()
   return render_template("index.html", message=message, enter=enter)


#Dashboard Handler *
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
   if not session.get('logged_in'):
      message = "Sign In"
      enter = "Enter"
      return render_template('index.html', message=message, enter=enter)
   if request.method == "POST":
      BookSearch = request.form.get("BookSearch")
      ResultNote = "Requested Book Not Found"
      BookResult = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn OR title LIKE :title OR author LIKE :author",{ "isbn": '%' + BookSearch + '%', "title": '%' + BookSearch + '%', "author": '%' + BookSearch + '%'}).fetchall()
      for BookSearch in BookResult:
         return render_template("books.html", BookResult=BookResult)
      return render_template ("dashboard.html", ResultNote=ResultNote)
      db.commit()  
   return render_template("dashboard.html")


#BookView Handler * 
@app.route("/booksview", methods=["GET", "POST"])
def booksview():
   if not session.get('logged_in'):
      message = "Sign In"
      enter = "Enter"
      return render_template('index.html', message=message, enter=enter)
   return render_template("dashboard.html")

#Rating Handler * 
@app.route("/rating/<string:isbn_id>", methods=["GET", "POST", "DELETE", "PUT"])
def rating(isbn_id):
   if not session.get('logged_in'):
      message = "Sign In"
      enter = "Enter"
      return render_template('index.html', message=message, enter=enter)
   ratings = db.execute("SELECT * FROM ratings WHERE isbn = :isbn",{"isbn":isbn_id}).fetchall()
   bookname = db.execute ("SELECT * FROM books WHERE isbn = :isbn", {"isbn":isbn_id}).fetchall()
   bookcheck = db.execute ("SELECT * FROM books WHERE isbn = :isbn", {"isbn":isbn_id}).rowcount
   rating_check = db.execute("SELECT * FROM ratings WHERE isbn = :isbn",{"isbn":isbn_id}).rowcount
   total = db.execute("SELECT AVG(rating) FROM ratings WHERE isbn = :isbn",{"isbn":isbn_id})
   total_id = average = db.execute("SELECT COUNT(rating) FROM ratings WHERE isbn = :isbn",{"isbn":isbn_id})
   key = "G4T2Wk4DpmmbsNmkzzfQA"
   secret = "uHcEUcRMyUygQfzE8hVCGmVmfr4buWhwD0dx24k"
   res = requests.get("https://www.goodreads.com/book/review_counts.json?",params={"isbns": isbn_id, "key": key})
   #Inner Check # 
   if bookcheck == 0:
      return render_template("dashboard.html", ratings=ratings, bookname=bookname, nonfound="No Rating Available yet for selected book")
   #Check good read
   if res.status_code != 200:
      nogoodread = "No information for the selected book on goodread"
      return render_template("rating.html", ratings=ratings, bookname=bookname, nogoodread=nogoodread)
   #Check Exisiting rating
   if rating_check == 0:
      jdata = res.json()
      for each in jdata["books"]:
         ratings_count = each['ratings_count']
         average_rating = each['average_rating']
         noreaderio = "No rating on reader.io for selected book"
      return render_template("rating.html", ratings=ratings, bookname=bookname, nogoodread=noreaderio, ratings_count=ratings_count, average_rating=average_rating)
   ##Action if Book has rating
   for isbn_id in total:
      total_val = round((isbn_id.avg),2)
   for count in total_id:
      count_val = count
   jdata = res.json()
   for each in jdata["books"]:
      ratings_count = each['ratings_count']
      average_rating = each['average_rating']
   return render_template("rating.html", ratings=ratings, bookname=bookname, average=total_val, count_val=count_val, ratings_count=ratings_count, average_rating=average_rating)
   db.commit()

#Submit Rating formform * 
@app.route("/rating", methods=["POST", "GET"])
def leavereview():
   if request.method == "GET":
      message = "Sign In"
      enter = "Enter"
      return render_template('index.html', message=message, enter=enter)
   if not session.get('logged_in'):
      message = "Sign In"
      enter = "Enter"
      return render_template('index.html', message=message, enter=enter)
   review = request.form.get("message")
   rating = request.form.get("rating")
   isbn = request.form.get("isbn")
   username = session['storing']
   if db.execute("SELECT * FROM ratings where username = :username AND isbn = :isbn",{"username":username, "isbn":isbn}).rowcount == 1:
   # if verify.rowcount is None:
      flash('You have previously rated this book')
      return redirect(request.referrer)
   storereview = db.execute("INSERT INTO ratings (isbn, review, username, rating) VALUES (:isbn, :review, :username, :rating)",{"isbn": isbn, "review": review, "username":username, "rating":rating})
   db.commit()
   flash('Thank you for successfully reviewing this book')
   return redirect(request.referrer)
  

#For Logout * Completed
@app.route('/logout')
def logout():
   message = "Sign In"
   enter = "Enter"
   session['logged_in'] = False
   return render_template("index.html", message=message, enter=enter)


#For API System * Remains Avg review
@app.route("/api/<string:api>")
def api(api):
   jvibes = db.execute("SELECT * FROM books WHERE isbn = :isbn",{"isbn":api})
   if jvibes.rowcount == 0:
      return jsonify({"error": "Invalid isbn_id"}), 422
   else:
      count = db.execute("SELECT * FROM ratings WHERE isbn = :isbn",{"isbn":api}).rowcount
      total = db.execute("SELECT AVG(rating) FROM ratings WHERE isbn = :isbn",{"isbn":api})
      readerio = db.execute("SELECT * FROM books WHERE isbn = :isbn",{"isbn":api}).fetchall()
      if count == 0:
         for api in readerio:
               title = api.title
               author = api.author
               isbn = api.isbn
               year = api.year
               return jsonify({"title": title,"author": author,"Total_review": count,"year": year, "Average":"No Average Ratings Available"})
      
      for api in total:
         average = json.dumps(Decimal(round((api.avg),2)), use_decimal=True)
    
      for api in readerio:
         title = api.title
         author = api.author
         isbn = api.isbn
         year = api.year
         return jsonify({"title": title, "author": author, "Total_review": count, "year": year, "average":average })


#Error Handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


## Designed with love by olusola
