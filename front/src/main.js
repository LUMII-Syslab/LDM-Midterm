import Vue from 'vue'
import underscore from 'vue-underscore'
import App from './App.vue'
import VueMoment from 'vue-moment'
import VueSession from 'vue-session'
import router from "./router"
// import Chartkick from 'vue-chartkick'
// import Chart from 'chart.js'
// import bFormSlider from 'vue-bootstrap-slider'

// import VueGoogleCharts from 'vue-google-charts'
 
import Default from "./layouts/Default.vue"
import NoBars from "./layouts/NoBars.vue"
// import VueFormJsonSchema from 'vue-form-json-schema';


import { TooltipPlugin } from 'bootstrap-vue'


import './assets/style.css';
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false
Vue.use(underscore);
Vue.use(VueSession);
Vue.use(VueMoment);
// Vue.use(Chartkick.use(Chart));

Vue.use(TooltipPlugin);
// Vue.use(bFormSlider)


// Vue.use(VueGoogleCharts);

Vue.component("default-layout", Default);
Vue.component("no-bars-layout", NoBars);
// Vue.component('vue-form-json-schema', VueFormJsonSchema);


const vue = new Vue({
	router,
	render: h => h(App),
}).$mount('#app')

window.Vue = vue;
