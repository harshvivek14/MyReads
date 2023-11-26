from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

# Connecting to the database in app
def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    # Data model for the user table
    __tablename__ = 'user'

    # Table columns
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(35), nullable=False)
    last_name = db.Column(db.String(35), nullable=False)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)


    # Relationships
    readlists = db.relationship('Readlist', backref="user_id_obj")
    shared_readlists = db.relationship('Shared_Readlist')

    @classmethod
    def register(cls, fname, lname, uname, pwd):
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")
        return cls(username=uname, password=hashed_utf8, first_name=fname, last_name=lname)

    @classmethod
    def authenticate(cls, uname, pwd):
        u = User.query.filter_by(username=uname).first()
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False
        
class Readlist(db.Model):
    __tablename__ = 'readlist'

    # Columns
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # FK on table user column id

    # Relationships
    books = db.relationship('Readlist_Books', cascade='all, delete')

class Shared_Readlist(db.Model):
    """Data model for shared readlists"""
    # Table name
    __tablename__ = 'shared_readlist'

    # Columns
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    readlist_id = db.Column(db.Integer, db.ForeignKey('readlist.id', ondelete="CASCADE")) # FK on table readlist column id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE")) # FK on table user column id
    # URL code must be unique because we don't want 2 readlist to have same URL
    url_code = db.Column(db.String(20), nullable=False, unique=True)

    # Relationships
    readlist = db.relationship('Readlist')

class Readlist_Books(db.Model):
    """Data model for readlist to book mapping"""
    # Table name
    __tablename__= 'readlist_books'

    # Columns
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    readlist_id = db.Column(db.Integer, db.ForeignKey('readlist.id', ondelete="CASCADE")) # FK on table readlist column id
    book_id = db.Column(db.String(20), nullable=False)

class Read_Books(db.Model):
    """Data model for marking books as read"""
    # Table Name
    __tablename__ = 'read_books'

    # Columns
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # FK on table user column id
    book_id = db.Column(db.String(20), nullable=False)

    # Relationships
    user = db.relationship('User', backref="read_books")
    