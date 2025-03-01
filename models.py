from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cx_Oracle
import os

# Database Info

DB_CONNECT_STRING = os.environ.get('DB_CONNECT_STRING')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://{}:{}@{}'.format(DB_USER,DB_PASSWORD,DB_CONNECT_STRING)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Contact(db.Model):

    __tablename__ = 'employees'

    id = db.Column(db.Integer, db.Identity(start=1), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(200), nullable=True, unique=True)
    phone = db.Column(db.String(20), nullable=True, unique=False)

    def __repr__(self):
        return '<Contacts %r>' % self.name