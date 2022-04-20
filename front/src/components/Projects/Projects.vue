<template>	
	<div>
		<div class="row">    
			<div class="col-lg-12">
				<div class="text-right">
					<button type="button" class="btn btn-primary btn-sm" data-toggle="modal" data-target="#new-project-modal"><i class="fas fa-plus"></i></button>
				</div>
			</div>
		</div>

		<br/>

		<div class="row">    
			<div class="col-lg-12">
				<div id="alerts_fail"  class="alert alert-danger collapse" role="alert">
					Project creation failed.
					<button type="button" class="close" data-dismiss="alert" aria-label="Close">
						<span aria-hidden="true">&times;</span>
					</button>
				</div>
					
				<div id="alerts_success" class="alert alert-success collapse" role="alert">
					Project created successfully.
					<button type="button" class="close" data-dismiss="alert" aria-label="Close">
						<span aria-hidden="true">&times;</span>
					</button>
				</div>

				<!-- The Modal -->
				<div class="modal" id="new-project-modal">
					<div class="modal-dialog">
						<div class="modal-content">

							<!-- Modal Header -->
							<div class="modal-header">
								<h4 class="modal-title">New project</h4>
								<button type="button" class="close" data-dismiss="modal">&times;</button>
							</div>

							<!-- Modal body -->
							<div class="modal-body">
								<div class="form-group">
									<label for="exampleInputEmail1">Name</label>
									<input type="text" class="form-control" id="project_name_id" placeholder="Enter project name">
								</div>

								<div class="form-group">
									<label for="exampleInputEmail1">Type</label>
									<select class="form-control" id = "project_type" disabled>
										<option value = "ImgClassification"> Image Classification</option>
										<option value = "ImgCaptioning"> Image Captioning</option>
									</select>		
								</div>
												
								<div class="form-group">
									<label for="exampleInputEmail1">Description</label>
									<input type="text" class="form-control" id="project_description_id" placeholder="Enter project description">	
								</div>
								
							</div>

							<!-- Modal footer -->
							<div class="modal-footer">
								<button type="button" class="btn btn-primary" data-dismiss="modal" @click="createNewProjectClicked">Create</button>
								<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
							</div>

						</div>
					</div>
				</div>

				<div class="row">
					<div class="col-xl-3 col-md-6 mb-4" v-for="p in projects" :key="p.id">
						<div class="card border-left-primary shadow h-100 py-2">
							<div class="card-body">
								<div class="row no-gutters align-items-center">
									<div class="col mr-2">
																
										<router-link :to="{name: 'Project', params: {project_id: p.id}}">
											<div class="h5 mb-0 font-weight-bold text-gray-800"> 
												{{ p.name }}
											</div>
										</router-link>

										<div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
											Author: {{p.owner_id}}
										</div>
										<div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
											Updated on: {{p.last_update_time}}
										</div>
										<div class="text-xs font-weight-bold text-primary text-uppercase mb-1"> 
											Num of runs: {{p.num_of_runs}}
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script src = "./Projects.js">