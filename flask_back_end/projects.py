import os, datetime

from flask import jsonify, request, make_response
from flask_login import current_user
from bson.objectid import ObjectId

from flask_pymongo import DESCENDING

import utilities as u

class Projects():

	def __init__(self, mongo, app):
		self.mongo = mongo
		self.config = {"SECRET_KEY": app.config['SECRET_KEY'],}


	def create_new_project(self, request):
		print(request.files)

		project_name = request.form.get('project_name') or "Project"

		response = make_response( 
		    jsonify({'msg': 'Malformed request. Param \'project_name\' must be present.'}),
		    400)

		proj_descr = ""
		if 'project_description' in request.form:
		    proj_descr = request.form.get('project_description')

		user_id = current_user.get_id()

		project = {'name': project_name, 
		            'user_id': ObjectId(user_id),
		            'description': proj_descr,
		            'created_at': datetime.datetime.utcnow()
		            }

		res = self.mongo.db.projects.insert_one(project)
		proj_id = str(res.inserted_id)

		project_out = {'id': proj_id, 
		                'name': project["name"], 
		                'owner_id': user_id,
		                'description': project["description"],
		                'last_update_time': project["created_at"],
		                'num_of_runs': 0,
		            }

		self.create_project_dirs(proj_id)

		return jsonify({'msg': 'project created successfully', 'data': project_out})


	def create_project_dirs(self, proj_id):
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects'))    
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id ))
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Runs' ))

		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Data'))
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Data', 'Train'))
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Data', 'Validation'))
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Data', 'Test'))
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Unzipped_data'))
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Unzipped_data', 'Train'))
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Unzipped_data', 'Validation'))
		u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Unzipped_data', 'Test'))


	def get_projects(self):
		user_id = current_user.get_id()
		projects = self.mongo.db.projects.find({'user_id': ObjectId(user_id)})

		output = []
		for curr_proj in projects:

		    num_of_runs = self.mongo.db.runs.find({'project_id' : ObjectId(curr_proj['_id'])}).count()
		    last_updated = "0:00"
		    if num_of_runs > 0:
		        #pedeja uzsakta run`a sakumlaiks
		        last_run = self.mongo.db.runs.find({'project_id' : ObjectId(curr_proj['_id'])}).sort('start_time', DESCENDING).limit(1)
		        last_updated = last_run[0]['start_time'] 
		    else:
		        if 'created_at' in curr_proj:
		            last_updated = curr_proj['created_at']
		            
		    output.append({
		        'id': str(curr_proj['_id']), 
		        'name': curr_proj['name'],
		        'last_update_time': last_updated,
		        'num_of_runs': num_of_runs,
		        'owner_id': str(curr_proj['user_id'])
		        })

		response = jsonify({'projects': output})

		return response