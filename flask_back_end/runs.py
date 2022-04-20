import os, datetime

from flask import jsonify, request, make_response
from flask_login import current_user
from bson.objectid import ObjectId
from bson.json_util import dumps

from flask_pymongo import DESCENDING

import utilities as u

class Runs():

	def __init__(self, mongo, app):
		self.mongo = mongo
		self.config = {"SECRET_KEY": app.config['SECRET_KEY'],}


	def get_runs(self, project_id):
		runs = self.mongo.db.runs.find({'project_id': project_id}).sort('start_time', DESCENDING)
		return make_response(dumps({'runs': runs,}))


	def get_run(self, run_id):
		logs = []
		run = self.mongo.db.runs.find_one({'_id': ObjectId(run_id)})
		if run is not None:
			logs = self.mongo.db.logs.find({'run_id': run_id})
		else:
			return 'No run, \'run_id\' ', 400

		return make_response(dumps({'run': run, 'logs': logs}))


	def edit_run(self, data_in):
		updated = self.mongo.db.runs.update_one({'_id': ObjectId(data_in["runId"]), "project_id": data_in["projectId"]},
												{"$set": {"comment": data_in["comment"],}})
		return make_response(dumps({}))


	def get_run_files(self, run_id):

		# files = [{""}]
		files = self.mongo.db.files.find({'run_id': run_id})

		return make_response(dumps({'files': files}))

	        # # collect files uploaded during this run
	        # proj_id = str(run['project_id'])
	        # files_on_disk = []
	        # run_path = os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Runs', run_id )
	        # if os.path.exists( run_path ):
	        #     for f in os.listdir( run_path ):
	        #         if os.path.isfile(os.path.join(run_path, f)):
	        #             files_on_disk.append(f)

	        # #[{'file_name':'a.txt', 'comment' : 'a', 'upload_time':''}]
	        # files_in_Mongo = self.mongo.db.files.find({'run_id' : ObjectId(run_id)})
	        # files_extended = []
	        # for mongo_file in files_in_Mongo:
	        #    if mongo_file['file_name'] in files_on_disk:
	        #         role_name = ""
	        #         if 'role_name' in mongo_file:
	        #             role_name = mongo_file['role_name']
	                                
	        #         files_extended.append( 
	        #             { 'file_name': mongo_file['file_name'], 
	        #               'comment' : mongo_file['comment'], 
	        #               'upload_time': mongo_file['upload_time'],
	        #               'role_name' : role_name
	        #             }
	        #         )


	        # # collect this project files
	        # #file_list = []
	        # #for f in os.listdir(os.path.join('./uploads', run_id,)):
	        # #    if os.path.isfile(os.path.join('./uploads', run_id, f)):
	        # #        file_list.append(f)

	        # gold_labels = self.get_gold_labels(str(run['project_id']))
	        # silver_labels = self.get_silver_labels(str(run['project_id']), run_id)

	        # # print("gold")
	        # # print(gold_labels)
	        # # print("silver")
	        # # print(silver_labels)

	        # res = []
	        # for k in gold_labels:
	        #     res.append((k, gold_labels[k], silver_labels.get(k)))
	        # # print(res)

	        # response = jsonify({'run': {'start_time': run['start_time'],
	                                    # 'finish_time': run['finish_time'] if 'finish_time' in run else "",
	                                    # 'logs': logs_output,
	                                    #'files': files_on_disk,
	                                    # 'files' : files_extended,
	                                    # 'gold': list(gold_labels),
	                                    # 'silver': silver_labels,
	                                    # 'file_gold_silver': res,
	                                    # 'project_id': str(run['project_id']),
	                                    # 'comment' : run['comment'],
	                                    # 'git_commit_url': run['git_commit_url'] if 'git_commit_url' in run else ""
	                                    # }})



	def start_run(self, project_id):
	    print("Recieved request from " + str(request.remote_addr) )
	    #find proj by name
	    proj = self.mongo.db.projects.find_one({'id': project_id})

	    print ("proj", proj)

	    # create run tied to this proj
	    if proj is not None:
	        proj_id = proj['_id']
	        
	        comment = ""
	        if 'comment' in request.args:
	            comment = request.args.get('comment')
	        
	        git_commit_url = ""
	        if 'git_commit_url' in request.args:
	            git_commit_url = request.args.get('git_commit_url')
	        
	        run = self.mongo.db.runs.insert_one({'project_id': proj_id,
	                                        'comment' : comment,
	                                        'start_time': datetime.datetime.now(),
	                                        'git_commit_url':git_commit_url,
	                                        'remote_address' : request.remote_addr
	                                        })
	        run_id = run.inserted_id
	        
	        u.ensure_dir_exists( os.path.join(u.get_app_root_dir(), 'Projects', str(proj_id), 'Runs', str(run_id)) )

	        return jsonify({'id': str(run_id)})
	    else:
	        print(name)
	        #return jsonify({'err': 'project named not found.'})
	        return jsonify({'err': 'Project named \'' + name + '\' not found.'}), 404


	def finish_run(self):
	    run_id = request.args.get('run_id')
	    if run_id is not None:
	        run = self.mongo.db.runs.find_one({'_id': ObjectId(run_id)})
	        if run is not None:

	            x = self.mongo.db.runs.update_one({'_id': ObjectId(run_id)},
	                                         {"$set": {"finished": True, 'finish_time': datetime.datetime.now()}}
	                                         )

	            return 'ok'
	        else:
	            return jsonify({'err': 'Run with id \'' + request.args['run_id'] + '\' not found.'}), 404
	    else:
	        #print(run_id)
	        #return jsonify({'err': 'project named not found.'})
	        return jsonify({'err': 'Malformed request. Param run_id must be present.'}), 404


	def log(self):
	    #check we have 2 args run_id and msg
	    if 'run_id' in request.args and 'msg' in request.args:
	        #check that run with id = run_id is present and is not finished
	        run = self.mongo.db.runs.find_one({'_id': ObjectId(request.args['run_id'])})
	        if run is None:
	            return jsonify({'err': 'Run with id \'' + request.args['run_id'] + '\' not found.'}), 404
	        elif 'finished' in run and run['finished']:
	            return jsonify({'err': 'Run with id \'' + request.args['run_id'] + '\' has been finished.'}), 403
	        else:
	            role_name = ""
	            if 'role_name' in request.args :
	                role_name = request.args['role_name']

	            # insert log message in to the given run
	            self.mongo.db.logs.insert_one(
	                {'run_id': request.args['run_id'], 
	                 'msg': request.args['msg'],
	                 'logged_on': datetime.datetime.utcnow(),
	                 'role_name' : role_name
	                }
	            )

	            print("logging msg " + request.args['msg'])
	            return 'ok'
	    else:
	        return jsonify({'err': 'Malformed request. Params run_id and msg must be present.'}), 404







	#TODO: rename to get_gold_labels from test-data
	def get_gold_labels(self, project_id):
	    # get first dir in os.path.join('./uploads', project_id, 'unzipped_data')
	    # from that dir get file labels.txt


	    if not os.path.isdir(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Test')):
	        return {}

	    first_dir = None
	    for dirn in os.listdir(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Test')):
	        print(dirn)
	        if os.path.isdir(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Test', dirn)):
	            first_dir = dirn
	            break
	    # print(first_dir)

	    file_name2label = {}
	    if first_dir is not None:
	        label_file_path = os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Test', first_dir, "labels.txt")
	        if os.path.isfile(label_file_path):
	            with open(label_file_path, "r") as f:
	                for line in f:
	                    parts = line.strip().split(',', 2)
	                    if len(parts) == 2:
	                        file_name2label[parts[0]]=parts[1]

	    print(file_name2label)
	    return file_name2label


	def get_silver_labels(self, project_id, run_id):
	    
	    label_file_path = os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Runs', run_id, 'silver_labels.txt' )
	    res = {}
	    if os.path.isfile(label_file_path):
	        with open(label_file_path, "r") as f:
	            for line in f:
	                parts = line.strip().split(',', 2)
	                if len(parts) == 2:
	                    res[parts[0]] = parts[1]
	    return res



	def get_human_readable_file_size(self, file_path):
	    size_in_bytes = 0
	    #check below  is necessary, get size returns size of a dir if file_path points to a dir
	    if os.path.isfile(file_path):        
	        size_in_bytes = os.path.getsize(file_path)
	    
	    if size_in_bytes // (1024*1024*1024) > 0 :
	        return str(size_in_bytes // (1024*1024*1024)) + " Gb"
	    elif size_in_bytes // (1024*1024) > 0:
	        return str(size_in_bytes // (1024*1024)) + " Mb"
	    elif  size_in_bytes // (1024) > 0:
	        return str(size_in_bytes // (1024)) + " Kb"
	    
	    return str(size_in_bytes ) + " bytes"