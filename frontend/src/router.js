import { createRouter, createWebHistory } from 'vue-router';
import AboutPage from '@/views/AboutPage.vue';
import SearchedLocation from '@/views/SearchedLocation.vue';
import UserFeed from '@/components/UserFeed.vue';
import SavedPlaces from '@/views/SavedPlaces.vue';
import MainPage from '@/views/MainPage.vue';
import ProfilePage from '@/views/ProfilePage.vue';
import GeneratedItinerary from '@/views/GeneratedItinerary.vue';
import LogIn from '@/views/LogIn.vue'; // Import LogIn component
import SignUp from '@/views/SignUp.vue';
import MyDestinations from '@/views/MyDestinations.vue';
import DestinationDetails from '@/views/DestinationDetails.vue';
import ExtractedLocations from '@/views/ExtractedLocations.vue';


import { getAuth, onAuthStateChanged } from 'firebase/auth';

// Combined routes from both HEAD and Dominic's branch
const routes = [
  { path: '/', name: 'MainPage', component: MainPage },  
  { path: '/about', name: 'AboutPage', component: AboutPage },
  { path: '/location', name: 'SearchedLocation', component: SearchedLocation },
  { path: '/feed', name: 'UserFeed', component: UserFeed },
  { path: '/log-in', name: 'LogIn', component: LogIn },
  { path: '/savedplaces', name: 'SavedPlaces', component: SavedPlaces },
  { path: '/profile', name: 'ProfilePage', component: ProfilePage },
  { path: '/generated', name: 'GeneratedItinerary', component: GeneratedItinerary },
  { path: '/sign-up', name: 'SignUp', component: SignUp },
  { path: '/destinations', name: 'MyDestinations', component: MyDestinations },
  {
    path: '/country/:country', // Ensure the param is named 'country'
    name: 'DestinationDetails',
    component: DestinationDetails,
    props: true, // Pass route params as props to the component
  },
  {
    path: '/extractedlocations',
    name: 'ExtractedLocations',
    component: ExtractedLocations,
  },

];

// Router instance with Firebase authentication logic
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
      if (!user && to.path !== '/log-in' && to.path !== '/sign-up') { // Redirect if not authenticated
        next('/log-in');
      } else {
        next(); // Proceed if authenticated or public route
      }
    });
  } else {
    const user = auth.currentUser;
    if (!user && to.path !== '/log-in' && to.path !== '/sign-up') {
      next('/log-in');
    } else {
      next();
    }
  }
});

export default router;
