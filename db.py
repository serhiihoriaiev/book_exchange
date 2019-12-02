from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class SiteUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    user_class = db.Column(db.String, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    library = db.relationship('Library', backref='user')


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    street_addr = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(40), nullable=False)
    region = db.Column(db.String(40), nullable=False)
    zip = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    users = db.relationship('SiteUser', backref='address')


lib_books = db.Table(
    'lib_books',
    db.Column('lib_id', db.Integer, db.ForeignKey('library.id'), primary_key=True),
    db.Column('book_id', db.String(100), db.ForeignKey('book.isbn'), primary_key=True)
)


class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('site_user.id'))
    books = db.relationship('Book', secondary=lib_books, backref='libraries')


class Book(db.Model):
    isbn = db.Column(db.String(100), primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    img_name = db.Column(db.String(100))
    genre = db.Column(db.String(100))
    year = db.Column(db.Integer)
    publisher = db.Column(db.String(100))
