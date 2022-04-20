<template>
	<div>
		
		<div class="modal" id="test-data-modal">
			<div class="modal-dialog">
				<div class="modal-content">

					<div class="modal-header">
						<h4 class="modal-title">Upload testing data</h4>
						<button type="button" class="close" data-dismiss="modal">&times;</button>
					</div>

					<div class="modal-body">
						<div class="form-group" >
							<div class="file-loading">
								<input id="test_file_input_id" name="test_file_input" type="file" ref="fileInputRef" accept=".zip">
							</div>	
						</div> 			
					</div>

					<div class="modal-footer">
						<button type="button" class="btn btn-primary" data-dismiss="modal" @click="uploadTestDataSetClicked">Upload</button>
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
					</div>
				</div>
			</div>
		</div>

		<div class="container_tabs_pills">			
			<ul class="nav nav-pills">
				<li class="nav-item">
					<router-link :to="{ name: 'Project', params: {project_id: projectId}}" class="nav-link" role="tab" data-toggle="tab">
						Runs
					</router-link>
				</li>
				<li class="nav-item">
					<li class="nav-item">
						<router-link :to="{ name: 'TrainingData', params: {project_id: projectId}}" class="nav-link active" role="tab" data-toggle="tab">
							Data 
						</router-link>
					</li>
				</li>		
			</ul>

			<div class="row">
				<div class="col-lg-12 text-right">
					<div class="btn-group" role="group">
						<button type="button" class="btn btn-primary btn-sm" data-toggle="modal" data-target="#test-data-modal"><i class="fas fa-upload"></i></button>
						<button type="button" class="btn btn-primary btn-sm" @click="download"><i class="fas fa-download"></i></button>
					</div>
				</div>
			</div>

			<div class="tab-content">
				<div class="tab-pane fade show active" id="tab-data">

					<ul class="nav nav-tabs" id="myTab" role="tablist">
						<li class="nav-item">
							<router-link id="training-data-tab" data-toggle="tab" class="nav-link" :to="{ name: 'TrainingData', params: {project_id: projectId }}" role="tab" aria-controls="training-data" aria-selected="false">
							Training data
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="validate-data-tab" data-toggle="tab" class="nav-link" :to="{ name: 'ValidateData', params: {project_id: projectId }}" role="tab" aria-controls="test-data" aria-selected="true">
							Validation data
							</router-link>
						</li>

						<li class="nav-item">
							<router-link id="test-data-tab" data-toggle="tab" class="nav-link active" :to="{ name: 'TestData', params: {project_id: projectId }}" role="tab" aria-controls="test-data" aria-selected="true">
							Test data
							</router-link>
						</li>
					</ul>

					<div class="tab-content" id="myTabContent2">
						<div class="tab-pane fade show active" id="test-data" role="tabpanel" aria-labelledby="home-tab">
							<div class="card shadow mb-4 col mr-2"> 
								<div class="card-body">

									<div class="row">
										<div class="col-lg-2">
											<!-- <label for="sel1" class="my-1 mr-2">Run</label> -->
					                    	<select class="form-control form-control-sm" @change="runChanged($event)" id="runs" v-model="runId">
					                        	<option value="None">None</option>
					                            <option v-for="run in runs" :value="run._id">{{run._id}}</option>
					                    	</select>
					                    </div>
										
										<div class="col-lg-10 text-right">
											<div class="btn-group" role="group" aria-label="Basic example">
												<button type="button" class="btn btn-primary btn-sm" data-toggle="modal" data-target="#test-data-modal"><i class="fas fa-upload"></i></button>
												<button type="button" class="btn btn-primary btn-sm" @click="download"><i class="fas fa-download"></i></button>
											</div>

											<div>
												<form class="form-horizontal">
													<p>Total {{totalImages}}</p>
												</form>
											</div>
										</div>
									</div>

						            <div v-if="!isLoading" class="row">
						                <div class="col-sm-9">        
						                    <div class="row">
						                        <div class="col" v-for="p in images">
							                        <!-- <img height="150" width="150" :src="p.path"> -->
							                        <!-- <div>Gold label: {{currClassName}}</div> -->
							                        <!-- <div>Silver label : Sunflower</div> -->
							                        <!-- <div>File name: {{p.name}}</div> -->


						                            <!-- <img height = "150" width = "150" :src=" SERVER_URL() + 'get_testing_file/' + p + `?project_id=` + project_id "  > -->
						                            <!-- <div> <span class = "font-weight-bolder h6" >Gold label : </span>{{currClassName}}</div> -->
						                            <div >
						                            	<img height="150" width="150" :src="p.path">

						                            	<div v-if="isDebugMode">
						                        			<div class="mb-3" :class="p.textStyle">
						                        				{{p.class}} / {{p.target}}
						                        			</div>
						                        		</div>
						     
						                        		<div v-else>
						                        			<div class="mb-3">
					                        					{{p.class}}
					                        				</div>
					                        			</div>
						                            </div>
						                        </div>
						                    </div>

											<nav aria-label="Page navigation example" >
						                        <ul class="pagination justify-content-center">
						                            <li class="page-item" v-bind:class="{ disabled: isPrevEnabled }"><a class="page-link" href="#" @click="prev">Previous</a></li>
						                            <!-- <li class="page-item"><a class="page-link" href="#">1</a></li> -->
						                            <!-- <li class="page-item"><a class="page-link" href="#">2</a></li> -->
						                            <!-- <li class="page-item"><a class="page-link" href="#">3</a></li> -->
						                            <li class="page-item" v-bind:class="{ disabled: isNextEnabled }"><a class="page-link" href="#" @click="next">Next</a></li>
						                        </ul>
											</nav>					    				
						                </div>


					                	<div class="col-sm-3">

						                    <div class="form-group">
						                        <fieldset id="fset1" @change="filterModeChanged($event)"  >
						                            <div class="form-check-inline">
						                                <label class="form-check-label" >
						                                    <input class="form-check-input" type="radio" name="binding" id="binding_provided" value="All" checked v-model="filter.active"> All
						                                </label>
						                            </div>
						                            
						                            <br/>
						                            
						                            <div class="form-check-inline">
						                                <label class="form-check-label" >
						                                    <input class="form-check-input" type="radio" name="binding" id="binding_weak" value="Matching" v-model="filter.active"> Matching (Gold == Silver)
						                                </label>
						                            </div>
						                            
						                            <br/>

						                            <div class="form-check-inline">
						                                <label class="form-check-label" >
						                                    <input class="form-check-input" type="radio" name="binding" id="binding_strong" value="Mismatching" v-model="filter.active"> Mismatching (Gold != Silver)
						                                </label>
						                            </div>
						                            
						                        </fieldset>
						                    </div>

						                    <hr>

						                    <div v-for="cl in labels" :key="cl._id">
						                        <span v-if="isDebugMode" class="font-weight-bolder h5">
						                            <input type="checkbox" class="label-checkbox" :id="cl._id" checked @click="checkboxClicked( cl, 'id' + cl )"> {{cl.category}}
						                            ({{cl.goldCount + "/" + cl.silverCount}})
						                        </span>

						                        <span v-else class="font-weight-bolder h5">
						                            <input type="checkbox" class="label-checkbox" :id="cl._id" checked @click="checkboxClicked( cl, 'id' + cl )"> {{cl.category}} ({{cl.goldCount}})
						                        </span>
						                    </div>

					                    	<br/>
					                    
					                    	<button type="button" class="btn btn-info mr-2" @click="selectAllCheckboxes()">Select all</button>
					                    	<button type="button" class="btn btn-default"  @click="clearAllCheckboxes()">Clear all</button>
					                  
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

<script src="./TestData.js"></script>