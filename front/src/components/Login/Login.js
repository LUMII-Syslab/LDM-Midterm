import { mymixin } from '../../mixins/mixins.js'

import { _ } from 'vue-underscore'
import utils from '../../utils/utils'

export default {
    mixins: [mymixin, utils],
    methods: {

        login(ev) {
            var self = this;

            var backend = this.SERVER_URL();
            var email = $("#email").val();
            var password = $("#password").val();

            console.log("backend ", backend)

            // if (!this.$session.exists()) {
            axios.post(backend + "login/", {"email": email, "password": password})
                .then(response => {

                    console.log("response ", response)

                    // TODO: error message should appear on the front page!
                    if (self.noErrorsInResponse(response)) {

                        var token = response.data.response.token;
 
                        console.log("token ", token)

                        localStorage.setItem("token", token);
                        localStorage.setItem("user", email);

                        self.$router.push('/projects');
                    }
                
    // {headers: {
    //         "Access-Control-Allow-Origin" : "*",
    //         "Content-type": "Application/json",
    //         "Authorization": `Bearer ${your-token}`
    //         }   
    //     }

                    // console.log("adsf a", self.$session.get("auth"))

                    // Vue.http.headers.common['Authorization'] = 'Bearer ' + token;
                    // self.$router.push('/app/shelf');

                })
                .catch(error => {
                    // TODO: show error on the front page
                    self.processErrorInPromise(error)
                });
        },
    }
};
