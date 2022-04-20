<template>
	<div>
		<div class="container_tabs_pills">			
			<ul class="nav nav-pills">
				<li class="nav-item">
					<router-link :to="{ name: 'Run', params: {run_id: runId}}" class="nav-link" role="tab" data-toggle="tab">
						Details
					</router-link>
				</li>
				<li class="nav-item">
					<li class="nav-item">
						<router-link :to="{ name: 'RunFiles', params: {run_id: runId}}" class="nav-link active" role="tab" data-toggle="tab">
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

							<div class="table-responsive">
								<table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
									<!-- <caption>Uploaded files : </caption> -->
									<thead>
										<tr>
											<!-- <th>#</th> -->
											<!-- <th>Role</th> -->
											<th>File</th>
											<th>Uploaded</th>
											<!-- <th>Comment</th> -->
										</tr>
									</thead>
									<tbody>
										<tr v-for="(file, i) in files" :key="file._id">
											<!-- <td>{{i + 1}}</td> -->
											<!-- <td>{{file.role_name}}</td> -->
											<td>
												<router-link :to="{ name: 'RunFile', params: {run_id: runId, file_name: file.file_name}}">{{file.file_name}}
												</router-link>


												<!-- <a :href="SERVER_URL() + 'get_file/' + file.file_name + '?run_id=' + runId" >{{file.file_name}}</a> -->
											</td>
											<td>{{file.uploaded_at}}</td>
											<!-- <td>{{file.comment}}</td> -->
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

<script src="./RunFiles.js"></script>