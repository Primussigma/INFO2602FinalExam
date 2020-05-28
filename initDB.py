from main import app
from models import db, User

db.create_all(app=app)

bob = User(username="bob", email = "bob@mail.com")
bob.set_password("bobpass")
john = User(username="john", email="john@mail.com")
john.set_password('johnpass')
db.session.add(bob)
db.session.add(john)
db.session.commit()

print('database initialized!')

