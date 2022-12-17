# Project 1

Web Programming with Python and JavaScript

* Program Designed to be light weight, so the pages do not contain any extra graphics or unncessary JS *

Firstly the requirements

•	Registration: Users should be able to register for your website, providing (at minimum) a username and password.
			* This page was built to be dynamic and would automatically change based on users preference, both contained in templates/index.html
			* I installed a passlib for added signin encrption
			* Once a username is taken, users cant register.


•	Login: Users, once registered, should be able to log in to your website with their username and password.
			* Users once registered can login at the homepage and would be redirected to a dashbpard where they can search 
			* A session user to is created to keep user details while assessing the website.

•	Logout: Logged in users should be able to log out of the site.
			* A logout component was built into to change session to false as an extra walk around, if users for anyreason goto the login screen, they would be required to signin again for added security protection

•	Import: Provided for you in this project is a file called books.csv, which is a spreadsheet in CSV format of 5000 different books. Each one has an ISBN number, a title, an author, and a publication year. In a Python file called import.py separate from your web application, write a program that will take the books and import them into your PostgreSQL database. You will first need to decide what table(s) to create, what columns those tables should have, and how they should relate to one another. Run this program by running python3 import.py to import the books into your database, and submit this program with the rest of your project code.

			* Code available at import.py, a fairly simple import script.


•	Search: Once a user has logged in, they should be taken to a page where they can search for a book. Users should be able to type in the ISBN number of a book, the title of a book, or the author of a book. After performing the search, your website should display a list of possible matching results, or some sort of message if there were no matches. If the user typed in only part of a title, ISBN, or author name, your search page should find matches for those as well!
			* A wildcard like%a% was used for this and users would be informed if no book like that exisit in my db. /dashboard is the route for this page
			* If book is available they would be redirected to /book route where possible matches would show.

•	Book Page: When users click on a book from the results of the search page, they should be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on your website.
			* Book page is the same as Rating page /rating, details would be seen prior to clicking the link
			* used a string:isbn for this purpose

•	Review Submission: On the book page, users should be able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users should not be able to submit multiple reviews for the same book.
			* At the route /rating you would see all the aforesaid entry and constraint
			* Except a book exisit, users would be redirected to dashboard if book doesnt exisit

•	Goodreads Review Data: On your book page, you should also display (if available) the average rating and number of ratings the work has received from Goodreads.
			* Good read api integrated into the system
			* if statements to prevent web app from bringing error if book details is not available

•	API Access: If users make a GET request to your website’s /api/<isbn> route, where <isbn> is an ISBN number, your website should return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. The resulting JSON should follow the format:

{
    "title": "Memory",
    "author": "Doug Lloyd",
    "year": 2015,
    "isbn": "1632168146",
    "review_count": 28,
    "average_score": 5.0
}
					* Same route was implemented, for api.
					* I had issues converting rowtable to actual useable value for json output as detail returned decimals and I didnt want to change db structure
					* A walk around was using the round function, acception decimals etal and adding if statement to show a different json for books without rating  simple json and decimal was used

If the requested ISBN number isn’t in your database, your website should return a 404 error.
					*Error implemented for books and routes not in db and application.

•	You should be using raw SQL commands (as via SQLAlchemy’s execute method) in order to make database queries. You should not use the SQLAlchemy ORM (if familiar with it) for this project.
					* Albeit stressful, learnt alot implementing this, esp the wildcard search and returning values for my average.

•	In README.md, include a short writeup describing your project, what’s contained in each file, and (optionally) any other additional information the staff should know about your project.
						* You have been reading my readme all along... hope you enjoyed reading.

•	If you’ve added any Python packages that need to be installed in order to run your web application, be sure to add them to requirements.txt!

						* You can find all in requirements.
						* FInally I cant wait to use ORMs for future projects, maybe I appreciate ORMs more now.


