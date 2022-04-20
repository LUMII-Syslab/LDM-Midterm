const default_layout = "default";

window.axios = require("axios");

export default {
  computed: {
    layout() {
      return (this.$route.meta.layout || default_layout) + "-layout";
    }
  }
}
