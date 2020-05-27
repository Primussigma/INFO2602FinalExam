from main import app
from models import db, User

db.create_all(app=app)

bob = User(username="bob", email = "bob@mail.com")
bob.set_password("bobpass")
john = User(username="john", email="john@mail.com")
john.set_password('johnpass')

print('database initialized!')