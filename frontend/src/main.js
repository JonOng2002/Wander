import App from './views/App.vue'
import { createApp } from 'vue'
import router from './router' // Assuming you have a router file

const app = createApp(App)
app.use(router) // Use the router
app.mount('#app')