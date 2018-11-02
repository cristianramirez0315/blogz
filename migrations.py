from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:criscr7madrid@localhost:8889/blogz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blogs = db.relationship('Blog', backref='owner')
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body, owner_id):
        self.owner_id = owner_id
        self.title = title
        self.body = body


if __name__ == '__main__':
    manager.run()
