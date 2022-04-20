import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

export default {
    mixins: [mymixin, utils],

    mounted: function() {
        var self = this;

        self.projectId = self.$route.params['project_id'];

        axios.get(this.SERVER_URL() + 'runs/' + self.projectId, self.getHeader(self))
                .then(function(response) {

                    console.log("response ", response)

                    if (response.status != 200) {
                        throw Error(response.statusText);
                    }

                    let data = response.data;

                    self.runs = _.map(data.runs, function(run) {
                                    _.extend(run, {_id: self.getId(run),
                                                    short_comment: self.makeShortComment(run.comment),
                                                });
                                    return run;
                                });

                })
                .catch(error => {
                    self.processErrorInPromise(error)
                });
    },

    data: function() {
        return {
            projectId: "",
            loading: false,
            activeRun: {},
            runs: [],
            error: null,
        }
    },

    methods: {            

        // this is a tmp solution
        addRun: function() {
            axios.post(this.SERVER_URL() + 'run/' + this.projectId, {}, this.getHeader(this))
                    .then(function(response) {      
                        console.log("bb", response)
                    })
                    .catch(error => {
                        self.processErrorInPromise(error)
                    });
        },

        makeShortComment: function(val) {
            return val.substr(0, 15) + "...";

        },

        editRun: function() {
            var self = this;

            var list = {runId: this.activeRun._id,
                        projectId: this.projectId,
                        comment: $("#edit-comment-field").val(),
                    };

            axios.put(this.SERVER_URL() + 'run', list, this.getHeader(this))
                    .then(function(response) {      
                        if (response.status != 200) {
                            console.error("Error", response);
                            return;
                        }

                        _.extend(self.activeRun, {comment: list.comment,
                                                    short_comment: self.makeShortComment(list.comment),
                                                });
                    })
                    .catch(error => {
                        self.processErrorInPromise(error)
                    });
        },

        deleteRun: function() {
            console.log("delete run")

            var list = {runId: this.activeRun._id,
                        projectId: this.projectId,
                    };

            console.log("in list", list)

            // axios.delete(this.SERVER_URL() + 'run/' + this.projectId, {}, this.getHeader(this))
            //         .then(function(response) {      
            //             console.log("bb", response)
            //         })
            //         .catch(error => {
            //             self.processErrorInPromise(error)
            //         }); 

        },

        setActiveRun: function(run_id) {
            this.activeRun = _.find(this.runs, function(run) {
                                return run._id == run_id;
                            });
        },

    },
}