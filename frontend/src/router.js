import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './views/HomePage.vue'; // Ensure your component path is correct
import AboutPage from './views/AboutPage.vue'; // Ensure your component path is correct
import AnalyseLink from './components/AnalyseLink.vue';
import SearchedLocation from './views/SearchedLocation.vue';

const routes = [
    { path: '/', component: AnalyseLink },
    { path: '/about', component: AboutPage },
    { path: '/home', component: HomePage },
    { path: '/location', component: SearchedLocation , props: (route) => ({ tiktokUrl: route.query.url }) },
];

const router = createRouter({
    history: createWebHistory(),  // Use Web History API for clean URLs
    routes,
});


export default router;