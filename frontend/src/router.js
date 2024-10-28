import { createRouter, createWebHistory } from 'vue-router';
import AboutPage from '@/views/AboutPage.vue';
import ExtractedLocation from '@/views/ExtractedLocations.vue';
import SavedPlaces from '@/views/SavedPlaces.vue';
import MainPage from '@/views/MainPage.vue';
import ProfilePage from '@/views/ProfilePage.vue';
import LogIn from '@/views/LogIn.vue'; // Import LogIn component
import SignUp from '@/views/SignUp.vue';
import MyDestinations from '@/views/MyDestinations.vue';
import DestinationDetails from '@/views/DestinationDetails.vue';
import CalendarPage from '@/views/CalendarPage.vue';
import TagsPage from '@/views/TagsPage.vue';
import GeneratedItinerary from '@/views/GeneratedItinerary.vue';
import MyItineraries from '@/views/MyItineraries.vue';
import LocationDate from '@/views/LocationDate.vue';
import { getAuth, onAuthStateChanged } from 'firebase/auth';


// Combined routes from both HEAD and Dominic's branch
const routes = [

  { path: '/', name: 'Home', component: MainPage },  
  { path: '/mainpage', name: 'MainPage', component: MainPage },  
  { path: '/about', name: 'AboutPage', component: AboutPage },
  { path: '/location', name: 'ExtractedLocation', component: ExtractedLocation },
  { path: '/savedplaces', name: 'SavedPlaces', component: SavedPlaces },
  { path: '/log-in', name:'LogIn', component: LogIn }, // Updated to use LogIn
  { path: '/profile', name: 'ProfilePage', component: ProfilePage },
  { path: '/sign-up', name: 'SignUp', component: SignUp },
  { path: '/destinations', name: 'MyDestinations', component: MyDestinations },
  {
    path: '/country/:country', // Ensure the param is named 'country'
    name: 'DestinationDetails',
    component: DestinationDetails,
    props: true, // Pass route params as props to the component
  }, 
  { path: '/locationdate', name: 'LocationDate', component: LocationDate },
  { path: '/calendar', name: 'CalendarPage', component: CalendarPage },
  { path: '/tags', name: 'TagsPage', component: TagsPage },
  { path: '/generatedItinerary', name: 'GenIti', component: GeneratedItinerary, },
  { path: '/myitineraries', name: 'MyItineraries', component: MyItineraries,
    props: (route) => ({
      itineraryGenerated: route.query.itineraryGenerated === 'true',
      itinerary: route.query.itinerary ? JSON.parse(route.query.itinerary) : []
    })
  },
];

// Router instance with Firebase authentication logic
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      };
    } else if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  },
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
