from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

wishlist_table = db.Table(
    'wishlist',
    db.Column('user_id', db.Integer, db.ForeignKey('site_user.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)


class SiteUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    group = db.Column(db.String, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    # avatar_name = db.Column(db.String(100))
    library = db.relationship('Library', backref='user', uselist=False)
    wishlist = db.relationship('Book', secondary=wishlist_table)
    # rating = db.Column(db.Float, default=0.00)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    street_addr = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(40), nullable=False)
    region = db.Column(db.String(40), nullable=False)
    zip = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    users = db.relationship('SiteUser', backref='address')


# association class that is used instead of Table because of additional fields 'hidden' and 'status'
class LibBooks(db.Model):
    lib_id = db.Column(db.Integer, db.ForeignKey('library.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    hidden = db.Column(db.Boolean, default=False)
    status = db.Column(db.String, default='Available for exchange')  # available for exchange or not
    book = db.relationship('Book')

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('site_user.id'))
    books = db.relationship('LibBooks')
    hidden_lib = db.Column(db.Boolean, default=False)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    translator = db.Column(db.String(100))
    # img_name = db.Column(db.String(100))
    genre = db.Column(db.String(100))
    year = db.Column(db.Integer)
    publisher = db.Column(db.String(100))
    isbn = db.Column(db.String(20))
    # rating = db.Column(db.Float, default=0.00)
