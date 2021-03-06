import json
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, login_required
from flask import Flask, request, render_template, redirect, flash, url_for
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 

from models import db, User, UserReact, Post #add application models

''' Begin boilerplate code '''

''' Begin Flask Login Functions '''
# login_manager = LoginManager()
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)

''' End Flask Login Functions '''

def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
  app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7) # uncomment if using flsk jwt
  CORS(app)
#   login_manager.init_app(app) # uncomment if using flask login
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()

''' End Boilerplate Code '''

''' Set up JWT here (if using flask JWT)'''
# using lab 5 code
def authenticate(uname, password):
  #search for the specified user
  user = User.query.filter_by(username=uname).first()
  #if user is found and password matches
  if user and user.check_password(password):
    return user

#Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
  return User.query.get(payload['identity'])

jwt = JWT(app, authenticate, identity)
''' End JWT Setup '''

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/app')
@jwt_required()
def client_app():
  return app.send_static_file('app.html')

@app.route('/posts', methods=["GET"])
@jwt_required()
def send_posts():
    queryPosts = Post.query.all()
    queryPosts = [p.toDict() for p in queryPosts]
    return json.dumps(queryPosts)

@app.route('/getUser', methods=["GET"])
@jwt_required()
def send_user():
    u = User.query.filter_by(id=current_identity.id).first()
    u = u.toDict()
    return json.dumps(u)

@app.route("/reactToPost", methods=["POST"])
@jwt_required()
def react_to_post():
    data = request.get_json()
    # check for existing react
    # if react exists then edit
    react = UserReact.query.filter_by(userId=current_identity.id, postId=data["postId"]).all()
    if react != None:
        react.react= data["react"]
    else:
        # else make new react
        react = UserReact(userId=current_identity.id, postId=data["postId"], react=data["react"])
        db.session.add(react)
    db.session.commit()
    return "react logged", 201

@app.route("/createPost", methods=["POST"])
@jwt_required()
def create_post():
    post = Post(userId=current_identity.id,text=request.data)
    db.session.add(post)
    db.session.commit()
    return "Post created", 201

@app.route("/deletePost", methods=["DELETE"])
@jwt_required()
def delete_my_post():
    queryPost= Post.query.filter_by(postId=request).first()
    db.session.delete(queryPost)
    db.session.commit()
    return "Post Deleted" , 204

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)

