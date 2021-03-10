from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Float, String, Integer, Column

#creating databank
db = SQLAlchemy()

#Class create a table ( with ORM)
class Info(db.Model):
    __tablename__='Info'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    text = Column(String(50))
    prob = Column(Float)


def create_app():
    app = Flask(__name__)

    app.config.update(SECRET_KEY= os.urandom(24))                 # secret key with 24 characters
    app.config['SQLALQUEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # create DB in memory

    db.init_app(app)                                              # initialize the db

    with app.app_context():
        db.create_all()                                           # create all tables (one in this case)

    from .pages import pages as pages_blueprint
    app.register_blueprint(pages_blueprint)                       # conect to pages

    return app




