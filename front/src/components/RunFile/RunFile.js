import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

export default{	 
    mixins: [mymixin, utils],
    mounted: function() {
        var self = this;

        self.runId = self.$route.params['run_id'];
        self.fileName = self.$route.params['file_name'];

        console.log("self.runId ", self.runId)
        console.log("self.fileName ", self.fileName)

        // axios.get(self.SERVER_URL() + 'run-files/' + self.runId, self.getHeader(self))
        //         .then(function(response) {

        //             console.log("response ", response)

        //             if (response.status != 200) {
        //                 throw Error(response.statusText);
        //             }
                    
        //             self.files = _.map(response.data.files, function(file) {
        //             				_.extend(file, {_id: self.getId(file),});
        //             				return file;
        //             			});
        //         })
        //         .catch(error => {
        //             self.processErrorInPromise(error)
        //         });
    },

	data: function() {
		return {
			runId: "",
            fileName: "",	
			error: null
		}
	},
	
	methods: {

	}		
};