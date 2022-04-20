import time, datetime, jwt
from flask import Flask, request, jsonify
from flask_login import UserMixin, current_user, login_user

from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

class User(UserMixin):

	def __init__(self, mongo, app):
		self.mongo = mongo
		self.config = {"SECRET_KEY": app.config['SECRET_KEY'],}
		self.id = None
		self.hashed_password = None
		self.email = None
		self.name = None
		self.surname = None
		self.role = None
		self.createdAt = None
		self.profileImage = None


	def select_by_email(self, email):
		user = self.mongo.db.Users.find_one({"email": email,})
		if (user):
			self.set_values(user)
		else:
			print ("No user", email)


	def select_logged_in_user_by_id(self, user_id):
		user = self.mongo.db.Users.find_one({"_id": ObjectId(user_id), "is_logged_in": True,})
		if (user):
			self.set_values(user)
		else:
			print ("No user", user_id)


	def set_values(self, user):
		self.id = str(user["_id"])
		self.hashed_password = user["password"]
		self.email = user["email"]
		# self.name = user["name"]
		# self.surname = user["surname"]
		# self.role = user["role"]
		self.createdAt = user["createdAt"]
		# self.profileImage = user["profileImage"]
		# self.followingTo = user["followingTo"]

	def check_password(self, password):
		return check_password_hash(self.hashed_password, password)

	def is_admin(self):
		return self.role == "admin"

	def get_email(self):
		return self.email

	def set_loggend_in(self, user_id):
		self.mongo.db.Users.update_one({"_id": ObjectId(user_id),}, {"$set": {"is_logged_in": True,}})


class Auth():

	def __init__(self, mongo, app):
		self.mongo = mongo
		self.config = {"SECRET_KEY": app.config['SECRET_KEY'],}
		self.logged_in = {}


	def hash_password(self, passw):
		return generate_password_hash(passw)


	def get_token(self, request):
		if 'Authorization' in request.headers:
			return {"status": 200, "token": request.headers['Authorization'].encode('ascii', 'ignore')}

		elif request.args.get('token'):
			return {"status": 200, "token": request.args.get('token')}

		else:
			return {"status": 500, "token": "-1",}


	def encode_auth_token(self, user_id):

		payload = {
			'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5, seconds=25),
			'iat': datetime.datetime.utcnow() + datetime.timedelta(days=5, seconds=25),
			'sub': user_id,
		}

		return jwt.encode(payload,
							self.config.get('SECRET_KEY'),
							algorithm='HS256'
						).decode("utf-8")


	def decode_auth_token(self, auth_token):
		token = auth_token
		if not isinstance(auth_token, str):
			token = auth_token.decode("utf-8")

		if (token == "-1" or token == -1):
			return {"status": False,}

		payload = jwt.decode(token, self.config.get('SECRET_KEY'))
		user_id = payload["sub"]

		if (user_id and user_id in self.logged_in and self.logged_in[user_id]):
			return {"status": True, "id": payload["sub"],}


	def set_loggend_in(self, user_id):
		self.logged_in[user_id] = True


	def is_logged_in(self, user_id):
		return self.logged_in[user_id]


	def logout_user(self):
		user_id = current_user.get_id()
		self.mongo.db.Users.update_one({"_id": ObjectId(user_id),}, {"$set": {"is_logged_in": False,}})
		self.logged_in[user_id] = False