
from flask_sqlalchemy import SQLAlchemy
from index import db
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    public_id = db.Column(db.String(), unique=True)
    name = db.Column(db.String(60))
    password = db.Column(db.String(80))

    def __init__(self):
        self.id = id 
        self.public_id = public_id
        self.name = name
        self.password = password

class Xss(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    payload = db.Column(db.String(400))
    

    def __init__(self,payload):
        self.payload = payload 


class Sql(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    payload = db.Column(db.String(400))
    

    def __init__(self,payload):
        self.payload = payload 


class Xxe(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    payload = db.Column(db.String(400))
    

    def __init__(self,payload):
        self.payload = payload 
       