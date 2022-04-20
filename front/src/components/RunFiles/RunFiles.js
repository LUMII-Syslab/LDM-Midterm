import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

export default{	 
	// props: ['run_id'],
    mixins: [mymixin, utils],

    mounted: function() {
        var self = this;

        self.runId = self.$route.params['run_id'];

        console.log("self.runId ", self.runId)


        axios.get(self.SERVER_URL() + 'run-files/' + self.runId, self.getHeader(self))
                .then(function(response) {

                    console.log("response ", response)

                    if (response.status != 200) {
                        throw Error(response.statusText);
                    }
                    
                    self.files = _.map(response.data.files, function(file) {
                    				_.extend(file, {_id: self.getId(file),});
                    				return file;
                    			});
                })
                .catch(error => {
                    self.processErrorInPromise(error)
                });
    },

	data: function() {
		return {
			runId: "",
			loading: false,					
			files: [],
			error: null
		}
	},
	
	methods: {

	}		
};