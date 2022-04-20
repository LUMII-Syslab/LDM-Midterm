import { _ } from 'vue-underscore';
import { EventBus } from '../components/event-bus.js';


export default {
  data: function() { return {
    modalNotification: null,
    }
  },
  methods: {
    processResponse(response) {
    	console.log("response", response);
    	return response.data; 
    	// return response.data.response;
    },

    getToken() {    
      return localStorage.getItem("token");
    },

    getId(obj) {
      if (obj._id && obj._id["$oid"]) {
        return obj._id["$oid"];
      }
      else {
        return obj._id;
      }
    },

    getUsername() {    
      return localStorage.getItem("user");
    },

    getHeader() {
    	var token = this.getToken();
    	console.log("token", token)

  		return {headers: {
      					Authorization: "Bearer " + token,
                "content-type": "application/json"
  					},
  				};
    },
	
  	TimeString(str) {
  		var timestr = this.$moment(str).format("YYYY-MM-DD HH:mm:ss");
  		return timestr == "0001-01-01 00:00:00" ? "" : timestr;
  	},

    addNotification(msg, type_in) {
      EventBus.$emit("add-notification", {msg: msg, type: type_in});
    },

    removeNotification(id) {
      EventBus.$emit("remove-notification", id);
    },

    removeAllNotifications() {
      EventBus.$emit("remove-all-notifications");
    },

    noErrorsInResponse(response, modal = false) {
      if (response.status == 200 && response.data.success != false) {
        return true;
      } else {
        var msg = response.status == 200 ? "Error in the "+response.config.url+" response! Status: OK, but \""+response.data.message+"\""
                                         : "Error in the "+response.config.url+" response! Status:"+response.status+", \""+response.statusText+"\"";
        modal ? this.showModalMessage(msg, "error")
              : this.addNotification(msg,"error"); 
        return false;
      }
    },

    processErrorInPromise(error, modal = false) {
      var msg = ""; 
      if (error.response) {
         msg = "Error in the endpoint "+error.response.config.url+
               ". Status:"+error.response.status+" \""+error.response.statusText+"\". Data: \""+error.response.data+"\"";
      } else {
         msg = error;
      }
      modal ? this.showModalMessage(msg, "error") : this.addNotification(msg, "error");
      
    },

    showModalMessage: function(msg, type_in) {
      const types = {
        info: "info",
        error: "danger",
        warning: "warning",
      };
      var type = types[type_in] || "info";
      this.modalNotification = {msg: msg, type: "alert-"+type };
    },

    clearModalMessage: function() {
      this.modalNotification = null;
    }
  
  }
}
