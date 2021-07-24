from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(64), primary_key=True)
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    isactive = db.Column(db.Boolean, default=0, nullable=False)
    isadmin = db.Column(db.Boolean, default=0, nullable=False)

    def __init__(self, id, fname, lname, email, password, isactive, isadmin):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password
        self.isactive = isactive
        self.isadmin = isadmin

class UserTodo(db.Model):
    __tablename__ = 'usertodo'
    id = db.Column(db.String(64), primary_key=True)
    todos = db.Column(db.ARRAY(db.TEXT), nullable=True)

    def __init__(self, id, todos):
        self.id = id
        self.todos = todos