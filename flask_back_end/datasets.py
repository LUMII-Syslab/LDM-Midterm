import os, datetime, zipfile, time, json

# import argparse, sys, os, json, time, datetime, math, re, uuid, zipfile

from flask import jsonify, request, make_response, send_from_directory, send_file
from flask_login import current_user
from bson.objectid import ObjectId
from bson.json_util import dumps

from werkzeug.utils import secure_filename
from flask_pymongo import DESCENDING

import utilities as u

class Datasets():

	def __init__(self, mongo, app):
		self.mongo = mongo
		self.config = {"SECRET_KEY": app.config['SECRET_KEY'],}
		self.data_limit = 20

	def upload_training_data(self, project_id):
		return self.upload_dataset(project_id, "Train", "training_data", "training_labels")


	def upload_testing_data(self, project_id):
		return self.upload_dataset(project_id, "Test", "test_data", "test_labels")


	def upload_validation_data(self, project_id):
		return self.upload_dataset(project_id, "Validation", "validation_data", "validation_labels")	


	def upload_dataset(self, project_id, data_type, data_collection, label_collection):
		if 'zip_file' in request.files:
			f = request.files['zip_file']
			zip_file_path = os.path.join(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Data', data_type, secure_filename(f.filename)))
			extract_dir = os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', data_type)

			f.save(zip_file_path)

			with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
			    zip_ref.extractall(extract_dir)

			images_out = []
			categories = []

			labels = self.get_gold_label_map(project_id)
			for category, values in labels.items():
				images = []
				for value in values:
					img = {"class": category, "src": value, "project_id": project_id,}
					images.append(img)

				images_ids = self.mongo.db[data_collection].insert_many(images)
				categories.append({"category": category, "project_id": project_id})

				images_out = images_out + u.merge_collection_with_ids(images, images_ids.inserted_ids)

			categories_ids = self.mongo.db[label_collection].insert_many(categories)
			categories_out = u.merge_collection_with_ids(categories, categories_ids.inserted_ids)

			return make_response(dumps({"images": images_out[:self.data_limit],
										"labels": categories_out,
										"totalImages": len(images_out),
										"step": self.data_limit,
									}))

		return 'Malformed request. Params \'zip_file\' and \'project_id\' must be present. ', 400


	def get_training_set(self, project_id):
		return self.get_dataset(project_id, "Train")


	def get_testing_set(self, project_id):
		return self.get_dataset(project_id, "Test")


	def get_validation_set(self, project_id):
		return self.get_dataset(project_id, "Validation")


	def get_dataset(self, project_id, dataset_type):
		dir_path = os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', dataset_type)
		filePaths = self.retrieve_file_paths(dir_path)

		zip_name = project_id + ".zip"

		zip_file = zipfile.ZipFile(zip_name, 'w')
		with zip_file:
			for file in filePaths:
				zip_file.write(file)

		return send_file(zip_name, attachment_filename = zip_name, as_attachment = True)


	def get_training_data(self, project_id, page_in):
		# this is tmp solution
		run_id = "none"
		return self.get_dataset_data(project_id, run_id, page_in, "training_data", "training_labels")


	def get_testing_data(self, project_id, run_id, page_in):
		return self.get_dataset_data(project_id, run_id, page_in, "test_data", "test_labels")


	def get_validation_data(self, project_id, run_id, page_in):
		return self.get_dataset_data(project_id, run_id, page_in, "validation_data", "validation_labels")


	def get_dataset_data(self, project_id, run_id, page_in, data_collection, label_collection):
		limit = self.data_limit
		page = int(page_in)

		images_collection = self.mongo.db[data_collection].find({"project_id": project_id})
		images = list(images_collection.skip(limit * page).limit(limit))

		labels = self.mongo.db[label_collection].find({"project_id": project_id})
		labels_count = self.mongo.db[data_collection].aggregate([{"$match": {"project_id": project_id},},
																{"$group" : {"_id": "$class", "count": {"$sum": 1}}}])
	
		silvers = []
		silvers_count = []
		if ((run_id).lower() != "none"):
			image_sources = []
			for image in images:
				image_sources.append(image["src"])

			silvers = self.mongo.db.silvers.find({"project_id": project_id, "run_id": run_id, "src": {"$in": image_sources}})
			silvers_count = self.mongo.db.silvers.aggregate([{"$match": {"project_id": project_id, "run_id": run_id,},},
															{"$group" : {"_id": "$class", "count": {"$sum": 1}}}])


		runs = self.mongo.db.runs.find({'project_id': project_id}).sort('start_time', DESCENDING)

		return make_response(dumps({"images": images,
									"labels": labels,
									"totalImages": images_collection.count(),
									"step": limit,
									"silvers": silvers,
									"runs": runs,
									"labelsCount": labels_count,
									"silversCount": silvers_count,
								}))


	def get_testing_data_silver_labels(self, project_id):
	    print("get testing data silver labels")
	    run_id = request.args.get('run_id')
	    print(project_id)
	    print(run_id)
	    labels_2_list_of_files,file_2_label = self.get_silver_label_map_for_test_data(project_id, run_id)
	    
	    response = make_response(jsonify({"labels_2_list_of_files":labels_2_list_of_files, "file_2_label":file_2_label }))
	    
	    return response




	def get_testing_file(self, name):
	    print("gettestingfile")
	    print(name)
	    project_id = request.args['project_id']
	    first_dir = None
	    for dirn in os.listdir(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Test')):
	        print(dirn)
	        if os.path.isdir(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Test', dirn)):
	            first_dir = dirn
	            break
	    # print(first_dir)
	    return send_from_directory(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Test', first_dir ), secure_filename(name), as_attachment=False)


	def get_training_data_set_chunk(self, project_id):
	    print(request.args)
	    fromInd = int(request.args['fromInd'])
	    toInd = int(request.args['toInd'])

	    data = []
	    # for i in range(fromInd,toInd):
	    #   data.append({"first": 'John', "last":'Doe', "suffix":"#" + str(i)})
	    
	    # response = make_response(jsonify({"data":data}))
	    # response.headers.add('Access-Control-Allow-Origin', '*')
	    

	    #return a list of file form proj dir 
	    
	    first_dir = None
	    for dirn in os.listdir(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Test')):
	        print(dirn)
	        if os.path.isdir(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Test', dirn)):
	            first_dir = dirn
	            break

	    print (first_dir)

	    if first_dir != None:
	        for file in os.listdir(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Test', first_dir)):
	            if( file.endswith(".jpg") or file.endswith(".jpeg")):
	                data.append(file)

	    print(data)

	    response = make_response(jsonify({"data":data[fromInd:max(toInd, len(data))]}))
	    
	    return response


	# stores file in a folder corresponding to given run_id
	def store_file(self, file, run_id):
	    #find project for this run
	    run = self.mongo.db.runs.find_one({'_id': ObjectId(run_id)})
	    if run is not None:
	        project_id = str(run['project_id'])
	    
	        # if dir for this run does not exist - create dir;
	        # after that store file in a dir corresponding to this run

	        run_dir_path = os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Runs', run_id)
	        #TODO: vai seit ir jabut ensure dir exists izsaukumam ?
	        u.ensure_dir_exists( run_dir_path )
	        file.save(os.path.join( run_dir_path, secure_filename(file.filename)))



	def get_gold_label_map(self, project_id):
	    #print("gold label map1")
	    if not os.path.isdir(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Train')):
	        return {}
	    #print("gold label map2")
	    # r=root, d=directories, f = files
	    labels_file_path = ""
	    for r, d, f in os.walk(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Train')):
	        for file in f:
	            #print("fname " + file)
	            if os.path.isfile(os.path.join(r, file)) and file == "labels.txt":
	                labels_file_path = os.path.join(r, file)
	    #print("lbfp " + labels_file_path)
	    if labels_file_path == "":
	        return {}
	    #print("gold label map3")
	    #print(labels_file_path)
	    labels_2_list_of_files = {}
	    with open(labels_file_path, "r") as f:
	        for line in f:
	            parts = line.strip().split(',', 2)
	            if len(parts) == 2:
	                fname = parts[0].strip()
	                label = parts[1].strip()
	                if not label in labels_2_list_of_files:
	                    labels_2_list_of_files[label] = []
	                labels_2_list_of_files[label].append(fname)
	    #print("gold label map ")
	    return labels_2_list_of_files


	def get_gold_label_map_for_test_data(self, project_id):
	    #print("gold label map1")
	    if not os.path.isdir(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Test')):
	        return {}
	    #print("gold label map2")
	    # r=root, d=directories, f = files
	    labels_file_path = ""
	    for r, d, f in os.walk(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Test')):
	        for file in f:
	            #print("fname " + file)
	            if os.path.isfile(os.path.join(r, file)) and file == "labels.txt":
	                labels_file_path = os.path.join(r, file)
	    #print("lbfp " + labels_file_path)
	    if labels_file_path == "":
	        return {}
	    #print("gold label map3")
	    #print(labels_file_path)
	    labels_2_list_of_files = {}
	    with open(labels_file_path, "r") as f:
	        for line in f:
	            parts = line.strip().split(',', 2)
	            if len(parts) == 2:
	                fname = parts[0].strip()
	                label = parts[1].strip()
	                if not label in labels_2_list_of_files:
	                    labels_2_list_of_files[label] = []
	                labels_2_list_of_files[label].append(fname)
	    #print("gold label map ")
	    return labels_2_list_of_files


	def get_silver_label_map_for_test_data(self, project_id, run_id):
	    #print("gold label map1")
	    if not os.path.isdir(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Runs', run_id)):
	        return None, None
	    #print("gold label map2")
	    # r=root, d=directories, f = files
	    labels_file_path = ""
	    for r, d, f in os.walk(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Runs', run_id)):
	        for file in f:
	            #print("fname " + file)
	            if os.path.isfile(os.path.join(r, file)) and file == "labels.txt":
	                labels_file_path = os.path.join(r, file)
	    #print("lbfp " + labels_file_path)
	    if labels_file_path == "":
	        return None, None
	    #print("gold label map3")
	    #print(labels_file_path)
	    labels_2_list_of_files = {}
	    file_2_label = {}
	    with open(labels_file_path, "r") as f:
	        for line in f:
	            parts = line.strip().split(',', 2)
	            if len(parts) == 2:
	                fname = parts[0].strip()
	                label = parts[1].strip()

	                file_2_label[fname] = label
	                
	                if not label in labels_2_list_of_files:
	                    labels_2_list_of_files[label] = []
	                labels_2_list_of_files[label].append(fname)
	    #print("gold label map ")
	    return labels_2_list_of_files, file_2_label


	def get_training_file(self, name, project_id):
	    # jasanem run id
	    # jaatgriez fails ./uploads/project_id/file_name
	    # project_id = request.args['project_id']
	    first_dir = None
	    for dirn in os.listdir(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Train')):
	        print(dirn)
	        if os.path.isdir(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Train', dirn)):
	            first_dir = dirn
	            break
	    # print(first_dir)
	    return send_from_directory(os.path.join(u.get_app_root_dir(), 'Projects', project_id, 'Unzipped_data', 'Train', first_dir ), secure_filename(name), as_attachment=True)



	def get_file(self, name):
	    # jasanem run id
	    # jaatgriez fails ./uploads/run_id/file_name
	    if 'run_id' in request.args and name is not None:
	        run_id = request.args['run_id']
	        proj_id = self.get_project_from_run(run_id)
	        if proj_id is not None:
	            return send_from_directory(os.path.join(u.get_app_root_dir(), 'Projects', proj_id, 'Runs', run_id), secure_filename(name), as_attachment=True)
	        else:
	            return "Project was not  found."

	    return "Error. Malformed request."


	def get_project_from_run(self, run_id):
	    run = self.mongo.db.runs.find_one({'_id': ObjectId(run_id)})
	    if run is not None:
	        project_id = str(run['project_id'])
	        return project_id
	    else:
	        return None


	def upload_file(self):
	    if 'file' in request.files and 'run_id' in request.args:
	        file = request.files['file']
	        run_id = request.args['run_id']
	        self.store_file(file, run_id)
	        #saglabat info par failu ieks Mongo
	        
	        comment = ""
	        if 'comment' in request.args:
	            comment = request.args.get('comment')

	        role_name = ""
	        if 'role_name' in request.args:
	            role_name = request.args.get('role_name')

	        self.mongo.db.files.insert_one(
	            {'file_name' : secure_filename(file.filename),
	             'run_id' : ObjectId(run_id),
	             'comment' : comment,
	             'upload_time' : datetime.datetime.utcnow(),
	             'role_name' : role_name
	             }
	        )
	             
	        return 'File uploaded successfully'

	    return 'Malformed request. No \'file\' found.'


	def upload(self):
	    if request.method == 'POST' and 'file' in request.files:
	        filename = uploadedFiles.save(request.files['file'])
	        print('a')
	        print(uploadedFiles.url(filename))
	        print('b')

	        return "uploaded successfully by flask-uploads"


	def retrieve_file_paths(self, dirName):

		# setup file paths variable
		filePaths = []

		# Read all directory, subdirectories and file lists
		for root, directories, files in os.walk(dirName):
			for filename in files:
			    # Create the full filepath by using os module.
			    filePath = os.path.join(root, filename)
			    filePaths.append(filePath)
		     
		return filePaths