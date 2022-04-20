<template>
	<div>
		<!-- <p>Start of component Run</p> <br> -->
		
		
		<div class="container_tabs_pills">			
			<ul class="nav nav-pills">
				<li class="nav-item">
					<router-link :to="{ name: 'Run', params: {run_id: runId}}" class="nav-link active" role="tab" data-toggle="tab">
						Details
					</router-link>
				</li>
				<li class="nav-item">
					<li class="nav-item">
						<router-link :to="{ name: 'RunFiles', params: {run_id: runId}}" class="nav-link" role="tab" data-toggle="tab">
							Files 
						</router-link>
					</li>
				</li>		
			</ul>

			<br/>

			<div class="tab-content" id="myTabContent2">
				<div class="tab-pane fade show active" id="test-data" role="tabpanel" aria-labelledby="home-tab">
					<div class="card shadow mb-4 col mr-2"> 
						<div class="card-body">

							<div class="row1">
								<p>RunId: {{run._id}}</p>
								<p>Comment: {{run.comment}}</p>
								<p>StartTime: {{run.start_time}}</p>

								<router-link :to="{ name: 'TrainingData', params: {project_id: run.project_id, run_id: run._id,}}">
									Results on training data
								</router-link>

								<router-link :to="{ name: 'ValidateData', params: {project_id: run.project_id, run_id: run._id,}}">
									Results on validation data
								</router-link>

								<router-link :to="{ name: 'TestData', params: {project_id: run.project_id, run_id: run._id,}}">
									Results on test data
								</router-link>

							</div>

							<div class="table-responsive">
								<table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
							
									<thead>
										<tr>
											<th>#</th>
											<th>Role</th>
											<th>Message ID</th>
											<th>Message</th>
											<th>Time</th>
											
										</tr>
									</thead>

									<tbody>
										<tr v-for="(log, i) in logs" :key="log._id">
											<td>{{ i + 1 }}</td>
											<td>{{ log.role_name }} </td>
											<td>{{ log._id }}</td>
											<td>{{ log.msg }}</td>
											<td>{{ log.logged_on }}</td>
										</tr>
									</tbody>
								</table>

							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

</template>

<script src="./Run.js"></script>