from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

autor_has_books = db.Table('autor_books',
							 db.Column('book_id', db.Integer, db.ForeignKey('books.book_id')),
                             db.Column('author_id', db.Integer, db.ForeignKey('authors.author_id'))
						   )

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	user_login = db.Column(db.String(25), unique=True, nullable=False)
	user_password = db.Column(db.String(25), unique=False, nullable=False)
	user_books = db.relationship('User_books', backref='user', lazy=True)


class Shelves(db.Model):
	shelves_id = db.Column(db.Integer, primary_key=True)
	shelves_name = db.Column(db.String(25), unique=False, nullable=False)
	user_books = db.relationship('User_books', backref='shelve', lazy=True)

class Publishers(db.Model):
	publishers_id = db.Column(db.Integer, primary_key=True)
	publishes_name = db.Column(db.String(50), nullable=False)
	books = db.relationship('Books', backref='publisher', lazy=True)

# CREATE TABLE categories (
# category_id Integer  PRIMARY KEY,
# category_name VARCHAR ( 50 ) NOT NULL,
# categors_id INTEGER references categories(category_id)
# );

class Categories(db.Model):
	category_id = db.Column(db.Integer, primary_key=True)
	category_name = db.Column(db.String, nullable=False)

	# categors_id = db.Column(db.Integer, db.ForeignKey('Categories.category_id'))
	books = db.relationship('Books', backref='category', lazy=True)

# CREATE TABLE books (
# books_id Integer  PRIMARY KEY,
# book_name VARCHAR ( 50 ) NOT NULL,
# description TEXT,
# page INTEGER,
# year INTEGER,
# publisher_id INTEGER references publishers(publisher_id ),
# categories_id INTEGER references categories(category_id )
# );

class Books(db.Model):
	book_id = db.Column(db.Integer, primary_key=True)
	book_name = db.Column(db.String, nullable=False)
	description = db.Column(db.Text)
	page = db.Column(db.Integer)
	year = db.Column(db.Integer)
	publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.publishers_id'))
	categories_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))

	user_books = db.relationship('User_books', backref='book', lazy=True)

# CREATE TABLE user_books (
# user_books_id Integer  PRIMARY KEY,
# price INTEGER ( 10 ) ,
# data_added DATE,
# data_readed DATE,
# rating SMALLINT,
# rewiew TEXT,
# status_id INTEGER references shelves(shelves_id ),
# user_id INTEGER references users(user_id ),
# book_id INTEGER references books(books_id )fr
# );

class User_books(db.Model):
	user_book_id = db.Column(db.Integer, primary_key=True)
	price = db.Column(db.Integer)
	data_added = db.Column(db.Date)
	data_readed = db.Column(db.Date)
	rating = db.Column(db.INTEGER)
	rewiew = db.Column(db.Text)
	status_id = db.Column(db.Integer, db.ForeignKey('shelves.shelves_id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))


# CREATE TABLE authors (
# author_id Integer  PRIMARY KEY,
# first_name VARCHAR ( 25 ) NOT NULL,
# second_name VARCHAR ( 25 ) NOT NULL
# );

class Authors(db.Model):
	author_id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(25), nullable=False)
	second_name = db.Column(db.String(25), nullable=False)

	book = db.relationship('Books', secondary=autor_has_books, backref=db.backref('autor'), lazy='dynamic')

# CREATE TABLE autor_has_books (
# id Integer  PRIMARY KEY,
# book_id INTEGER references books(books_id ),
# author_id INTEGER references authors(author_id )
# );
