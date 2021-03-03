from flask import Flask ,request, jsonify , make_response, redirect
import json

from flask_marshmallow import Marshmallow
import os 
import random
import uuid
from werkzeug.security import generate_password_hash , check_password_hash
import jwt 
import datetime
from .db import Sql

'''
********************************
           Flask Api
********************************
'''
#init app
app = Flask(__name__)



'''
********************************
        Database stuff
********************************
'''
#db base dir
base_dir = os.path.abspath(os.path.dirname(__file__))
#db config
app.config['SECRET-KEY'] = 'mysecretkey'
key = app.config['SECRET-KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
#db init 

class PayloadSchema(ma.Schema):
    class Meta:
        fields = ('payload')    
  
payload_schema = PayloadSchema()


'''
********************************
            Routes
********************************
'''

#add payload
@app.route('/add_payload' ,methods=['POST'])
def add_payload():
    payload = request.json['payload']
    #add new payload to db
    new_load = Payload(payload)
    db.session.add(new_load)
    db.session.commit()
    return payload_schema.jsonify(new_load)

#show payload
@app.route('/api/xss/', methods=['GET'])
def view_payloads():
    ran = random.randint(1,4500)
    id_str = str(ran)
    payload = Payload.query.get(id_str)

    return payload_schema.jsonify(payload)

#show payload
@app.route('/api/sql/', methods=['GET'])
def view_payloads():
    ran = random.randint(1,4500)
    id_str = str(ran)
    payload = Payload.query.get(id_str)

    return payload_schema.jsonify(payload)


#show payload
@app.route('/api/xxe/', methods=['GET'])
def view_payloads():
    ran = random.randint(1,4500)
    id_str = str(ran)
    payload = Payload.query.get(id_str)

    return payload_schema.jsonify(payload)    

#user routes 
#gets all users
@app.route('/user' ,methods=['GET'])
def  get_all_users():
    users = User.query.all()
    #makes an object that will be appended to
    output = []
    #itterate user info
    for user in users:
        #user dic
        user_data = {}
        #user info from db  
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        #appends user info
        output.append(user_data)

    return jsonify({"users": output})



#gets one user using id 
@app.route('/user/<public_id>', methods=['GET'])
def  get_one_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    #makes an object that will be appended to
    if not user:
        return jsonify({"Error":"No user found"})

    #itterate user info
    user_data = {}
        #user info from db  
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin
    #appends user info

    return jsonify({"user": user_data})


#make a new user 
@app.route('/user', methods=['POST'])
def  create_users():
    #get json data
    data = request.get_json()
    print(data)
    #hash pass
    hash_pass = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'],password=hash_pass , admin=False)
    db.session.add(new_user)
    db.session.commit() 
    return jsonify({ "response" : "New user added" })


#promote user to admin
@app.route('/user/_boss/<public_id>', methods=['PUT'])
def  promote_users(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    #makes an object that will be appended to
    if not user:
        return jsonify({"Error":"No user found"})
    user.admin = True
    db.session.commit()  
    return jsonify({"Congrats":"Welcome New Admin"})  



#delete user
@app.route('/user/<public_id>', methods=['DELETE'])
def delete_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    #makes an object that will be appended to
    if not user:
        return jsonify({"Error":"No user found"})
    db.session.delete(user)
    db.session.commit()

    return jsonify({"Done":"User has been deleted"})

#login 
@app.route('/login' )
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not be authed' , 401, {'WWW-Authenticate':'Basic Realm = "Please just log in"'})
    
    user = User.query.filter_by(name=auth.username).first()
  
    
    if not user:
        return make_response('Could not be authed' , 401, {'WWW-Authenticate':'Basic Realm = "Please just log in"'})
    #checks user pass and auth pass to make a api token 
    if check_password_hash(user.password, auth.password):
        #make a jwt token using public id 
        time=datetime.datetime.utcnow()+datetime.timedelta(minutes=15)
        time_delta = str(time)
       
        token=jwt.encode({'public_id': user.public_id , 'exp':time_delta}, key)
        #returns token 
        print(token)
        return jsonify({'token':token.decode('UTF-8')})
    return make_response('Could not be authed' , 401, {'WWW-Authenticate':'Basic Realm = "Please just log in"'})


'''
********************************
            Server
********************************
'''
#server
if __name__ == "__main__":
    app.run("127.0.0.1", "4382" ,debug=True)
