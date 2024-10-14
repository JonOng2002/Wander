import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './views/HomePage.vue';
import AboutPage from './views/AboutPage.vue';
import AnalyseLink from './components/AnalyseLink.vue';
import SearchedLocation from './views/SearchedLocation.vue';
import SavePlaceButton from './components/SavePlaceButton.vue';
import Signin from './components/SignIn.vue';
import UserFeed from './components/UserFeed.vue';
import RegisterAcc from './components/RegisterAcc.vue';

import { getAuth, onAuthStateChanged } from 'firebase/auth';

const routes = [
  { path: '/', component: AnalyseLink },
  { path: '/about', component: AboutPage },
  { path: '/home', component: HomePage },
  { path: '/location', component: SearchedLocation },
  { path: '/savePlace', component: SavePlaceButton },
  { path: '/register', component: RegisterAcc },
  { path: '/feed', component: UserFeed },
  { path: '/signin', component: Signin },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

let isAuthResolved = false;

router.beforeEach((to, from, next) => {
  const auth = getAuth();
  if (!isAuthResolved) {
    onAuthStateChanged(auth, (user) => {
      isAuthResolved = true;
      if (!user && to.path !== '/signin' && to.path !== '/register') {
        next('/signin'); // Redirect to login if not authenticated
      } else {
        next(); // Proceed to the route if authenticated
      }
    });
} else {
    const user = auth.currentUser;
    if (!user && to.path !== '/signin' && to.path !== '/register') {
      next('/signin'); // Redirect to login if not authenticated
    } else {
      next(); // Proceed to the route if authenticated
    }
  }
});

export default router;