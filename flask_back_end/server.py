#!/usr/bin/env python
# import argparse, sys, , json, time, datetime, math, re, uuid, zipfile

import os, datetime, json

from bson import ObjectId
from flask import Flask, render_template, request, jsonify, make_response
from flask_pymongo import PyMongo
from flask_login import LoginManager, login_required, logout_user, login_user


import jwt

from functools import wraps
import auth, users, projects, runs, datasets
import utilities as u


# MONGO_URI_LOCAL       = "mongodb://localhost:27017/logging_db"
# MONGO_URI_CONTAINER   = "mongodb://mongo:27017/logging_db"
# MONGO_URI_LOCAL_paper = "mongodb://localhost:27017/logging_db_raksts"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some-secret-string12345reqfgb'

# MONGO_URI_LOCAL       = "mongodb://mongo:27017/logging_db"
# MONGO_URI_CONTAINER   = "mongodb://mongo:27017/logging_db"
# MONGO_URI_LOCAL_paper = "mongodb://mongo:27017/logging_db_raksts"

# mongo_uri_prm = ""
# if len(sys.argv) > 1:
# 	mongo_uri_prm = sys.argv[1]


# print ("mongo_uri_prm ", mongo_uri_prm)

# set_app(app)
#app.config["MONGO_URI"] = "mongodb://mongo:27017/logging_db"
# if mongo_uri_prm != "" :
# print("Using user supplied mongo URI \'" + mongo_uri_prm + "\'")
app.config["MONGO_URI"] = "mongodb://mongo:27017/logging_db"
# else:
	# print("Using default mongo URI \'mongodb://localhost:27017/logging_db\'")
	# app.config["MONGO_URI"] = MONGO_URI_LOCAL_paper

mongo = PyMongo(app)

Auth = auth.Auth(mongo, app)
Users = users.Users(mongo, app, Auth)

Projects = projects.Projects(mongo, app)
Runs = runs.Runs(mongo, app)
Datasets = datasets.Datasets(mongo, app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')

    return response


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user1(user_id):
	user = auth.User(mongo, app)
	user.select_logged_in_user_by_id(user_id)

	return user

@login_manager.request_loader
def load_user2(request):
	token = request.headers.get('Authorization')
	token_obj = Auth.get_token(request)
	if (token_obj["status"] == 200):
		token = token_obj["token"]
		resp = Auth.decode_auth_token(token)
		if resp and resp["status"]:
			user_id = resp["id"]

			user = auth.User(mongo, app)
			user.select_logged_in_user_by_id(user_id)

			return user
	# 	else:
	# 		return jsonify(**{"status": 500, "response": []})

	# else:
	return jsonify(**{"status": 500, "response": []})


#////////////////////////////////////////////////////////////// ROUTES //////////////////////////////////////////////////////////////////////////////////////////////////

def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is missing.'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message':'Token is invalid'}), 403

        return f(*args, **kwargs)

    return decorated


@app.route('/')
def hello_world():
    return jsonify({'status': 200, 'msg': "Super cool app is running..."})


@app.route('/start_run/<project_id>')
# @require_token
@login_required
def start_run(project_id):
    return Runs.start_run(project_id)


@app.route('/finish_run')
# @require_token
@login_required
def finish_run():
    return Runs.finish_run()


@app.route('/log')
# @require_token
@login_required
def log():
    return Runs.log()


@app.route('/get_logs')
def view_logs():
    output = []
    logs = None
    if 'project_id' in request.args:
        logs = mongo.db.logs.find({'project_id': request.args['project_id']})
    else:
        logs = mongo.db.logs

    for l in logs:
        role_name = ""
        if 'role_name' in l:
            role_name = l['role_name']
        
        output.append({'id': str(l['_id']), 'msg': l['msg'], 'role_name': role_name})
    print(output)

    response = jsonify({'res': output})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/projects')
@login_required
def get_projects():
	return Projects.get_projects()


@app.route('/runs/<project_id>')
@login_required
def get_runs(project_id):
    return Runs.get_runs(project_id)


@app.route('/run/<run_id>')
@login_required
def get_run(run_id):
    return Runs.get_run(run_id)


@app.route('/run-files/<run_id>')
@login_required
def get_run_files(run_id):
    return Runs.get_run_files(run_id)


@app.route('/upload', methods=['POST'])
@login_required
def upload():
    return Datasets.upload()


@app.route('/upload_file', methods=['POST'])
@require_token
def upload_file():
    return Datasets.upload_file()


@app.route('/upload-training-data/<project_id>', methods=['POST'])
@login_required
def upload_training_data(project_id):
    return Datasets.upload_training_data(project_id)


@app.route('/upload-test-data/<project_id>', methods=['POST'])
@login_required
def upload_testing_data(project_id):
    return Datasets.upload_testing_data(project_id)


@app.route('/upload-validation-data/<project_id>', methods=['POST'])
@login_required
def upload_validation_data(project_id):
    return Datasets.upload_validation_data(project_id)


@app.route('/project', methods=['POST'])
@login_required
def create_new_project():
	return Projects.create_new_project(request)


@app.route('/get_file/<name>')
@login_required
def get_file(name):
    return Datasets.get_file(name)


@app.route('/get-training-file/<name>/<project_id>')
@login_required
def get_training_file(name, project_id):
    return Datasets.get_training_file(name, project_id)


@app.route('/get-training-set/<project_id>')
@login_required
def get_training_set(project_id):
    return Datasets.get_training_set(project_id)


@app.route('/get-test-set/<project_id>')
@login_required
def get_testing_set(project_id):
    return Datasets.get_testing_set(project_id)


@app.route('/get-validation-set/<project_id>')
@login_required
def get_validation_set(project_id):
    return Datasets.get_validation_set(project_id)


@app.route('/get_training_data_set_size/<string:project_id>')
@login_required
def get_data_set_size(project_id):
    return jsonify({"size":50})


@app.route('/get_training_data_set_chunk/<string:project_id>')
@login_required
def get_training_data_set_chunk(project_id):
    return Datasets.get_training_data_set_chunk(project_id)


@app.route('/get_testing_file/<string:name>')
@login_required
def get_testing_file(name):
    return Datasets.get_testing_file(name)

@app.route('/training-data/<project_id>/<page>')
@login_required
def get_training_data(project_id, page):
    return Datasets.get_training_data(project_id, page)


@app.route('/testing-data/<project_id>/<run_id>/<page>')
@login_required
def get_testing_data(project_id, run_id, page):
    return Datasets.get_testing_data(project_id, run_id, page)

@app.route('/validation-data/<project_id>/<run_id>/<page>')
@login_required
def get_validation_data(project_id, run_id, page):
    return Datasets.get_validation_data(project_id, run_id, page)


@app.route('/get_testing_data_silver_labels/<string:project_id>')
@login_required
def get_testing_data_silver_labels(project_id):
    return Datasets.get_testing_data_silver_labels(project_id)


@app.route('/register', methods=["POST"])
def register_user():
    data_in = json.loads(request.data.decode("utf-8"))
    Users.add_user(data_in)

    return jsonify(**{"status": 200, "response": []})


@app.route('/login/', methods=["POST", "GET"])
def post_login_user():
    data_in = request.get_json(force=True)

    email = data_in['email']
    password = data_in['password']

    user = auth.User(mongo, app)
    user.select_by_email(email)
    check = user.check_password(password)
    if (check):
        login_user(user, remember=True)
        user_id = user.get_id()
        user.set_loggend_in(user_id)
        Auth.set_loggend_in(user_id)
        token = Auth.encode_auth_token(user_id)

        return {"status": 200, "response": {"token": token, "_id": user.get_id(), "role": user.role,}}
    else:
        return {"status": 401, "response": "Login failed",}


@app.route("/logout")
@login_required
def logout():
    Auth.logout_user()
    logout_user()
    return jsonify(**{"status": 200, "response": []})



@app.route("/run", methods=["PUT"])
@login_required
def edit_run():
    data_in = json.loads(request.data.decode("utf-8"))
    return Runs.edit_run(data_in)


#//////////////////////////////////////////////////////////////END OF ROUTES//////////////////////////////////////////////////////////////////////////////////////////////////

@app.route("/run/<project_id>", methods=["POST"])
@login_required
def add_run(project_id):
    from flask_login import current_user

    run = mongo.db.runs.insert_one({'project_id': project_id,
                                    'comment' : "this is comment1",
                                    'start_time': datetime.datetime.now(),
                                    'git_commit_url': "commit_url1",
                                    'remote_address' : "address1",
                                    'user_id': current_user.get_id(),
                                })
    run_id = run.inserted_id
    
    u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', str(project_id), 'Runs', str(run_id)) )


# logs
    mongo.db.logs.insert_one(
        {'run_id': str(run_id), 
         'project_id': project_id,
         'msg': "Message1",
         'logged_on': datetime.datetime.utcnow(),
         'role_name' : "role"
        }
    )


    mongo.db.logs.insert_one(
        {'run_id': str(run_id),
         'project_id': project_id,
         'msg': "Message2",
         'logged_on': datetime.datetime.utcnow(),
         'role_name' : "role"
        }
    )


# files
    mongo.db.files.insert_one(
        {'run_id': str(run_id),
         'project_id': project_id,
         'file_name': "File1.py",
         'uploaded_at': datetime.datetime.utcnow(),
        }
    )


    mongo.db.files.insert_one(
        {'run_id': str(run_id),
         'project_id': project_id,
         'file_name': "File2.py",
         'uploaded_at': datetime.datetime.utcnow(),
        }
    )

    mongo.db.files.insert_one(
        {'run_id': str(run_id),
         'project_id': project_id,
         'file_name': "File3.py",
         'uploaded_at': datetime.datetime.utcnow(),
        }
    )


# results
    mongo.db.silvers.insert_one({"class": 'bluebell',
                                    "src": 'image_0241.jpg',
                                    "project_id": project_id,
                                    "run_id": str(run_id),
                                    "created_at": datetime.datetime.utcnow(),
                                })

    mongo.db.silvers.insert_one({"class": 'bluebell',
                                    "src": 'image_0242.jpg',
                                    "project_id": project_id,
                                    "run_id": str(run_id),
                                    "created_at": datetime.datetime.utcnow(),
                                })

    mongo.db.silvers.insert_one({"class": 'bluebell',
                                    "src": 'image_0243.jpg',
                                    "project_id": project_id,
                                    "run_id": str(run_id),
                                    "created_at": datetime.datetime.utcnow(),
                                })

    mongo.db.silvers.insert_one({"class": 'cowslip',
                                    "src": 'image_0244.jpg',
                                    "project_id": project_id,
                                    "run_id": str(run_id),
                                    "created_at": datetime.datetime.utcnow(),
                                })

    mongo.db.silvers.insert_one({"class": 'bluebell',
                                    "src": 'image_0245.jpg',
                                    "project_id": project_id,
                                    "run_id": str(run_id),
                                    "created_at": datetime.datetime.utcnow(),
                                })

    mongo.db.silvers.insert_one({"class": 'cowslip',
                                    "src": 'image_0246.jpg',
                                    "project_id": project_id,
                                    "run_id": str(run_id),
                                    "created_at": datetime.datetime.utcnow(),
                                })

    return jsonify(**{"status": 200, "response": []})



def setUpDB():
	print("setup db")
	# mongo = get_mongo()
	num_of_docs = mongo.db.Users.find({}).count()
	if num_of_docs == 0:
		print("users table is empty - inserting ")
		mongo.db.users.insert_one(
			{
				"login":"user1",
				"password":"psw1",
				"name":"User1 Name"
			}
		)
	col = mongo.db.users.find({})
	for e in col:
		print(e)
	print("/setup db")
	return


if __name__ == '__main__':
	# mongo_uri_prm = ""
	# if len(sys.argv) > 1:
	# 	mongo_uri_prm = sys.argv[1]

	# # set_app(app)
	# #app.config["MONGO_URI"] = "mongodb://mongo:27017/logging_db"
	# if mongo_uri_prm != "" :
	# 	print("Using user supplied mongo URI \'" + mongo_uri_prm + "\'")
	# 	app.config["MONGO_URI"] = mongo_uri_prm
	# else:
	# 	print("Using default mongo URI \'mongodb://localhost:27017/logging_db\'")
	# 	app.config["MONGO_URI"] = MONGO_URI_LOCAL_paper

	# mongo = PyMongo(app)
	# set_mongo( mongo )

	#print(app)
	
	#print ( app.url_map )
	# setUpDB()

    app.run(debug=False, host='0.0.0.0', threaded=True)
