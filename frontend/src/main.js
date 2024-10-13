import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS
import 'bootstrap/dist/js/bootstrap.bundle.js'; // Import Bootstrap JS (includes Popper.js)

// Import BootstrapVue3 and its CSS
import BootstrapVue3 from 'bootstrap-vue-3';
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'; // Correct import for BootstrapVue3 CSS

// import { createRouter, createWebHistory } from 'vue-router';
// import { createStore } from 'vuex';
import { vue3GoogleLogin } from 'vue3-google-login';

const app = createApp(App);
app.use(router); // Use the router in the app
app.use(BootstrapVue3); // Use BootstrapVue3
app.use(vue3GoogleLogin, {
    clientId: '534126756340-2vokn8in9452u0m1uretrg6n1it4cgni.apps.googleusercontent.com'
})

app.mount('#app');
