import { createRouter, createWebHistory } from 'vue-router';
import AboutPage from './views/AboutPage.vue';
// import AnalyseLink from './components/AnalyseLink.vue';
import SearchedLocation from './views/SearchedLocation.vue';
import UserFeed from './components/UserFeed.vue';
import SavedPlaces from './views/SavedPlaces.vue';
import MainPage from '@/views/MainPage.vue';
import ProfilePage from '@/views/ProfilePage.vue'; 
import ItineraryPage from '@/views/ItineraryPage.vue';
import GeneratedItinerary from '@/views/GeneratedItinerary.vue';
import LogIn from '@/views/LogIn.vue'; // Import your LogIn component
import SignUp from '@/views/SignUp.vue';

import { getAuth, onAuthStateChanged } from 'firebase/auth';

// Combined routes from both HEAD and jiaxin
const routes = [
//   { path: '/', component: AnalyseLink },
  { path: '/about', component: AboutPage },
  { path: '/location', component: SearchedLocation },
  { path: '/feed', component: UserFeed },
  { path: '/log-in', component: LogIn }, // Updated to use LogIn
  { path: '/savedPlaces', component: SavedPlaces },
  
  // Routes from jiaxin branch
  { path: '/', name: 'MainPageAlias', component: MainPage },
  { path: '/profile', name: 'ProfilePage', component: ProfilePage },
  { path: '/itinerary', name: 'ItineraryPage', component: ItineraryPage },
  { path: '/generated', name: 'GeneratedItinerary', component: GeneratedItinerary },
  { path: '/sign-up', name: 'SignUp', component: SignUp },
];

// Keep the authentication logic from the HEAD branch
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
      if (!user && to.path !== '/log-in' && to.path !== '/sign-up') { // Change to /log-in
        next('/log-in'); // Redirect to login if not authenticated
      } else {
        next(); // Proceed to the route if authenticated
      }
    });
  } else {
    const user = auth.currentUser;
    if (!user && to.path !== '/log-in' && to.path !== '/sign-up') { // Change to /log-in
      next('/log-in'); // Redirect to login if not authenticated
    } else {
      next(); // Proceed to the route if authenticated
    }
  }
});

export default router;