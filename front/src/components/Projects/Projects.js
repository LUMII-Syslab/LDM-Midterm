import { mymixin } from '../../mixins/mixins.js'

import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

export default {
    mixins: [mymixin, utils],
    mounted: function() {
    	var self = this;

        axios.get(this.SERVER_URL() + 'projects', self.getHeader(self))
	            .then(function(response) {

		            if (response.status != 200) {
		                throw Error(response.statusText);
		            }

		            self.projects = response.data.projects;
		        })
	            .catch(error => {
	                self.processErrorInPromise(error)
	            }); 
    },

    data: function() {
        return {
            projects: [],
        };
    },

	methods: {
		createNewProjectClicked: function() {
			var self = this;

			$('#alerts_success').hide();
			$('#alerts_fail').hide();

			//let fileToUpload = this.$refs.fileInputRef.files[0];
			let formData = new FormData();
			
			formData.append('project_name', document.getElementById("project_name_id").value);
			formData.append('project_description', document.getElementById("project_description_id").value);

			let header = self.getHeader(self);
            axios.post(this.SERVER_URL() + "project", formData, header)
					.then(response => {	

						if (response.status != 200) {
							$('#alerts_fail').show();
							return;
						}

						$('#alerts_success').show();
						self.projects = _.union(self.projects, [response.data.data]);
					},
					response => {						
						console.log(response.body)				
						$('#alerts_fail').show();
					});
		},
	}
};
