import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

export default{	 
	// props: ['run_id'],
    mixins: [mymixin, utils],

    mounted: function() {
        let self = this;

        self.runId = self.$route.params['run_id'];

        console.log("self.runId ", self.runId)


        axios.get(self.SERVER_URL() + 'run/' + self.runId, self.getHeader(self))
                .then(function(response) {

                    console.log("response ", response)

                    if (response.status != 200) {
                        throw Error(response.statusText);
                    }
                    
                    let run = response.data.run;
                    _.extend(run, {_id: self.getId(run),});

                    console.log("run", run)

                    self.run = run;

                    self.logs = _.map(response.data.logs, function(log) {
                    				_.extend(log, {_id: self.getId(log)})
                    				return log;
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
			run: {},
			logs: [],
			error: null
		}
	},
	created () {
		// fetch the data when the view is created and the data is
		// already being observed
		//console.log('f data called')
		// this.fetchData()
	},
	// watch: {
	// 	// call again the method if the route changes
	// 	'$route': 'fetchData'
	// },		
	methods: {

		// getPost( run_id ){		
		// 	console.log(run_id);
		// 	var loc_run = 
		// 		fetch( this.SERVER_URL()  + 'run/' + run_id)
		// 	    .then(response=>response.json())
	 //      		.then(json => {
	 //        			this.run = json.run
	 //      		})
		// 	return this.run;
		// },
		
		// fetchData () {
		// 	this.error = this.post = null
		// 	this.loading = true
		// 	// replace `getPost` with your data fetching util / API wrapper
		// 	var res = this.getPost(this.run_id);
			
		// 	this.loading = false
		// 	this.run = res;
			
		// }
	}		
};