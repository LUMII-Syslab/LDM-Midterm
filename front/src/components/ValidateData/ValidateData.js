import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

export default {
    mixins: [mymixin, utils],

    mounted: function() {
        this.projectId = this.$route.params['project_id'];
        this.runId = this.$route.params['run_id'] || this.runId;

        if (this.$route.params['run_id']) {
            this.isDebugMode = true;
        }

        this.getData();
    },

    data: function() {
        return {
            projectId: "",
            runId: "None",
            runs: [],
            currentPage: 0,
            step: 1,
            totalImages: 0,
            labels: {},
            images: [],
            isLoading: false,
            isPrevEnabled: "disabled",
            isNextEnabled: "disabled",
            isDebugMode: false,
            filter: {active: "All",},
        }
    },

    methods: {

        getData: function() {
            let self = this;
            axios.get(self.SERVER_URL() + 'validation-data/' + self.projectId + "/" + self.runId + "/" + self.currentPage, self.getHeader(self))
                    .then(function(response) {

                        console.log("response ", response)


                        let data = self.processData(response);
                        _.extend(self, data);
                        self.checkPaginationButtons();
                    })
                    .catch(error => {
                        self.processErrorInPromise(error);
                    });
        },

        processData: function(response) {
            let self = this;

            if (response.status != 200) {
                self.processErrorInPromise(response);
                return;
            }

            let data = response.data;

            let labels_map = {};
            _.each(data.labelsCount, function(label) {
                labels_map[label._id] = label.count;
            });


            let silvers_map = {};
            _.each(data.silversCount, function(label) {
                silvers_map[label._id] = label.count;
            });


            let labels = _.map(data.labels, function(label) {
                                                return {_id: self.getId(label),
                                                        category: label.category,
                                                        goldCount: labels_map[label.category],
                                                        silverCount: silvers_map[label.category] || 0,
                                                    };
                                            });

            let silvers = {};
            _.each(data.silvers, function(silver) {
                silvers[silver.src] = silver.class;
            });


            let images = _.map(data.images, function(img) {
                                let path = self.SERVER_URL() + 'get-training-file/' + img.src + "/" + img.project_id;

                                let text_style_class = "text-warning";
                                let silver_value = silvers[img.src];

                                if (silver_value) {
                                    text_style_class = "text-success";
                                    if (silver_value != img.class) {
                                        text_style_class = "text-danger";
                                    }
                                }

                                return {_id: self.getId(img),
                                        name: img.src,
                                        class: img.class,
                                        path: path,
                                        target: silver_value || "no-value",
                                        textStyle: text_style_class,
                                    };
                            });


            let runs = _.map(data.runs, function(run) {
                            _.extend(run, {_id: self.getId(run),});
                            return run;
                        });

            return {labels: labels,
                    images: images,
                    totalImages: data.totalImages,
                    step: data.step,
                    silvers: silvers,
                    runs: runs,
                };
        },

        uploadValidationDataSetClicked: function() {
            let self = this;
        
            let form_data = new FormData();
            form_data.append('zip_file', this.$refs.fileInputRef.files[0]);
        
            axios.post(this.SERVER_URL() + 'upload-validation-data/' + this.projectId, form_data, this.getHeader(this))
                    .then(function(response) {  
                        var data = self.processData(response);
                        _.extend(self, {totalImages: self.totalImages + data.totalImages,
                                        images: data.images,
                                        labels: _.union(self.labels, data.labels),
                                    });
                        self.checkPaginationButtons();
                    })
                    .catch(error => {
                        self.processErrorInPromise(error)
                    });
        },
        
        download: function() {
            let self = this;

            let header = self.getHeader(self);
            _.extend(header, {responseType: 'blob'});

            axios.get(self.SERVER_URL() + 'get-validation-set/' + self.projectId, header)
                    .then(function(response) {
                        let fileURL = window.URL.createObjectURL(new Blob([response.data]));
                        let fileLink = document.createElement('a');

                        fileLink.href = fileURL;
                        fileLink.setAttribute('download', "validation_" + self.projectId + '.zip');
                        document.body.appendChild(fileLink);

                        fileLink.click();
                    })
                   .catch(error => {
                        self.processErrorInPromise(error);
                    });
        },

        prev: function(e) {
            e.preventDefault();
            this.currentPage = Math.max(0, this.currentPage - 1);
            this.getData();
            this.checkPaginationButtons();
        },

        next: function(e) {
            e.preventDefault();
            this.currentPage = Math.min(this.currentPage + 1, Math.ceil(this.totalImages / this.step));
            this.getData();
            this.checkPaginationButtons();
        },

        checkPaginationButtons: function() {

            if (this.currentPage > 0) {
                this.isPrevEnabled = "";
            }
            else {
                this.isPrevEnabled = "disabled";
            }


            if (this.currentPage < Math.ceil(this.totalImages / this.step)) {
                this.isNextEnabled = "";
            }
            else {
                this.isNextEnabled = "disabled";
            }
        },

        runChanged: function(event) {
            let run_id = event.target.value;
            if (run_id == "None") {
                run_id = undefined;
            }

            this.$router.push({name: 'ValidateData', params: {project_id: this.projectId, run_id: run_id,}});

            this.runId = run_id;
            if (this.runId) {
                this.isDebugMode = true;
            }
            else {
                this.isDebugMode = false;
            }

            this.getData();

            this.runId = this.runId || "None";
        },

        clearAllCheckboxes: function() {
            $(".label-checkbox").removeAttr("checked");
        },

        selectAllCheckboxes: function() {
            $(".label-checkbox").attr("checked", "checked");
        },

        filterModeChanged: function($ev) {
            let active = $ev.target.value;
            _.extend(this.filter, {active: active});

            // this.getData();
        },

    }
}