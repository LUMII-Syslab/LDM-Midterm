import { mymixin } from '../../mixins/mixins.js'

import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

export default {
    mixins: [mymixin, utils],
    mounted: function() {    
    	// console.log("in mount data")

     //    axios.get(this.SERVER_URL() + 'get_projects?user=1')
	    //         .then(function(response) {
		   //          if (!response.ok) {
		   //              throw Error(response.statusText);
		   //          }
		   //          return response;
		   //      })
		   //      .then(response=>response.json())
		   //      .then(json => {
		   //              console.log("in json ", json)
		   //              this.projects = json.projects
		   //      }).catch(function(error) {
		   //          console.log(error);
		   //      });
    },
};
