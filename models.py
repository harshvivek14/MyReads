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
    # id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(35), nullable=False)
    last_name = db.Column(db.String(35), nullable=False)
    username = db.Column(db.String(15), nullable=False, unique=True, primary_key=True)
    password = db.Column(db.Text, nullable=False)

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