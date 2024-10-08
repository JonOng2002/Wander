import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS
import 'bootstrap/dist/js/bootstrap.bundle.js'; // Import Bootstrap JS (includes Popper.js)

// Import BootstrapVue3 and its CSS
import BootstrapVue3 from 'bootstrap-vue-3';
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'; // Correct import for BootstrapVue3 CSS

const app = createApp(App);
app.use(router); // Use the router in the app
app.use(BootstrapVue3); // Use BootstrapVue3

app.mount('#app');
