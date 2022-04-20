<template>
	<div>
		<div class="container_tabs_pills">			
			<ul class="nav nav-pills">
				<li class="nav-item">
					<router-link :to="{ name: 'Project', params: {project_id: projectId }}" class="nav-link active" role="tab" data-toggle="tab">
						Runs 
					</router-link>
				</li>
				<li class="nav-item">
					<router-link :to="{ name: 'TrainingData', params: {project_id: projectId }}" class="nav-link" role="tab" data-toggle="tab">
						Data 
					</router-link>
				</li>		
			</ul>

			<br/>

			<div class="tab-content">
				<div class="tab-pane fade active show" id="tab-project-runs">
					<div class="card shadow mb-4">
						<div class="card-body">
							<div class="table-responsive">
								<table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">

									<thead>
										<tr>
											<th>#</th>
											<th>Run ID</th>
											<th>Comment</th>
											<th>Start datetime</th>
											<th>End datetime</th>
											<th>IP</th>
											<th>User ID</th>
											<th>Commit URL</th>
											<th></th>
											<th></th>
										</tr>
									</thead>

									<tbody>
										<tr :id="run._id" class="run" v-for="(run, ind) in runs" :key="run._id">
											<td>{{ind + 1}}</td>
											<td>
												<router-link :to="{name: 'Run', params: {run_id: run._id}}">{{run._id}}</router-link>
											</td>
											<td>{{run.short_comment}}</td>
											<td>{{run.start_time}}</td>
											<td>{{run.finish_time}}</td>
											<td>{{run.remote_address}}</td>
											<td>{{run.user_id}}</td>
											<td>
												<a :href="run.git_commit_url">{{run.git_commit_url}}</a>
											</td>
											<td>
												<a href="#" data-toggle="modal" data-target="#edit-modal" @click="setActiveRun(run._id)">
													<i class="fas fa-edit"></i>
												</a>
											</td>
											<td>
												<a href="#" data-toggle="modal" data-target="#delete-modal">
													<i class="fas fa-trash"></i>
												</a>
											</td>
										</tr>
									</tbody>

								</table>
							</div>

							<button @click="addRun">Add run</button>

						</div>
					</div>
				</div>
			</div>
		</div>


		<div class="modal" id="edit-modal">
			<div class="modal-dialog">
				<div class="modal-content">

					<!-- Modal Header -->
					<div class="modal-header">
						<h4 class="modal-title">Edit</h4>
						<button type="button" class="close" data-dismiss="modal">&times;</button>
					</div>

					<!-- Modal body -->
					<div class="modal-body">
						<div class="form-group">
							<label for="edit-comment-field">Comment</label>
							<input type="text" class="form-control" id="edit-comment-field" :value="activeRun.comment">
						</div>						
					</div>

					<!-- Modal footer -->
					<div class="modal-footer">
						<button type="button" class="btn btn-primary" data-dismiss="modal" @click="editRun">Edit</button>
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
					</div>

				</div>
			</div>
		</div>
	</div>

</template>

<script src="./Project.js"></script>