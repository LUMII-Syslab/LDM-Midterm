import { mymixin } from '../../mixins/mixins.js'
import { _ } from 'vue-underscore';
import utils from '../../utils/utils'

export default {
    name: "TopBar",
    mixins:[mymixin, utils],
    data: function() {
        return {user: this.getUsername(),}
    },

    methods: {

        logout(ev) {
            var self = this;

            axios.get(this.SERVER_URL() + "logout", self.getHeader())
                    .then(response => {

                        if (self.noErrorsInResponse(response)) {

                            self.$session.destroy();
                            localStorage.clear();

                            self.$router.push('/');
                        }
                    });
        },

    }
}