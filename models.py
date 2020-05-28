from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()
import datetime


class User(db.Model):
    # copied code from Lab 5
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def toDict(self):
      return {
        "id": self.id,
        "username": self.username,
        "email": self.email,
        "password": self.password
      }
    
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class UserReact(db.Model):
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    postId = db.Column(db.Integer, db.ForeignKey('post.id') , primary_key=True)
    react = db.Column(db.String(80), default = 'like' or 'dislike')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False )
    text = db.Column(db.String(2048), nullable=False)
    reacts = db.relationship('UserReact', backref='Post', lazy=True)

    def getTotalLikes(self):
        numLike = 0
        reacts =  UserReact.query.filter_by(postId = self.id ).react
        for react in reacts :
            if (react == "like"): numLike += 1
        return numLike    

    def getTotalDislikes(self):
        numDislike = 0
        reacts =  UserReact.query.filter_by(postId = self.id ).react
        for react in reacts :
            if (react == "dislike"): numDislike += 1
        return numDislike

    def toDict(self):
        return {
        "postId": self.id,
        "userId": self.userId,
        "username": User.query.filter_by(id = self.userId).username,
        "text": self.text,
        "likes": getTotalLikes(),
        "dislikes": getTotalDislikes()
      }
