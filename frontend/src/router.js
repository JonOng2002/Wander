import { createRouter, createWebHistory } from 'vue-router';
import AboutPage from '@/views/AboutPage.vue';
import ExtractedLocation from '@/views/ExtractedLocations.vue';
import SavedPlaces from '@/views/SavedPlaces.vue';
import MainPage from '@/views/MainPage.vue';
import ProfilePage from '@/views/ProfilePage.vue';
import GeneratedItinerary from '@/views/GeneratedItinerary.vue';
import SavedItinerary from '@/views/SavedItinerary.vue';
import ItineraryDetails from '@/views/ItineraryDetails.vue';
import LogIn from '@/views/LogIn.vue'; // Import LogIn component
import SignUp from '@/views/SignUp.vue';
import MyDestinations from '@/views/MyDestinations.vue';
import DestinationDetails from '@/views/DestinationDetails.vue';
import CalendarPage from '@/views/CalendarPage.vue';
import TagsPage from '@/views/TagsPage.vue';
// import TrvPartner from '@/views/TravellingWithWho.vue';
import ItineraryBuilder from '@/views/ItineraryBuilder.vue';
import LocationDate from '@/views/LocationDate.vue';
import { onAuthStateChanged } from 'firebase/auth';
import OverlayPage from '@/views/overlayPage.vue';
import NotFound from '@/views/NotFound.vue'; // Create a NotFound.vue component
import { auth } from './main'


// Combined routes from both HEAD and Dominic's branch
const routes = [

  { path: '/', name: 'Home', component: MainPage },   
  { path: '/about', name: 'AboutPage', component: AboutPage },
  { path: '/location', name: 'ExtractedLocation', component: ExtractedLocation },
  { path: '/savedplaces', name: 'SavedPlaces', component: SavedPlaces },
  { path: '/log-in', name:'LogIn', component: LogIn }, // Updated to use LogIn
  { path: '/profile', name: 'ProfilePage', component: ProfilePage },
  { path: '/myitinerary', name: 'GeneratedItinerary', component: GeneratedItinerary },
  { path: '/saveditinerary', name: 'SavedItinerary', component: SavedItinerary },
  {
    path: '/itinerary-details/:savedAt',  // ':id' is the dynamic parameter for the itinerary ID
    name: 'ItineraryDetails',
    component: ItineraryDetails,
  props: true,
  },
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
  { path: '/itineraryBuilder', name: 'ItineraryBuilder', component: ItineraryBuilder,
    props: (route) => ({
      itineraryGenerated: route.query.itineraryGenerated === 'true',
      itinerary: route.query.itinerary ? JSON.parse(route.query.itinerary) : []
    })
  },
  { path: '/overlay', name: 'OverlayPage', component: OverlayPage },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
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
  if (!isAuthResolved) {
    // Use onAuthStateChanged to resolve the authentication state
    onAuthStateChanged(auth, (user) => {
      isAuthResolved = true; // Mark as resolved
      handleNavigation(user, to, next);
    });
  } else {
    // If auth state is already resolved, use auth.currentUser
    handleNavigation(auth.currentUser, to, next);
  }
});

function handleNavigation(user, to, next) {
  if (user) {
    // If the user is authenticated and tries to access /log-in or /sign-up, redirect to main page
    if (to.path === '/log-in' || to.path === '/sign-up') {
      next('/');
    } else {
      next(); // Proceed if the user is authenticated and the route is not /log-in or /sign-up
    }
  } else {
    // If the user is not authenticated, redirect to /log-in unless they are accessing /sign-up
    if (to.path !== '/log-in' && to.path !== '/sign-up') {
      next('/log-in');
    } else {
      next(); // Allow access to /log-in or /sign-up
    }
  }
}

export default router;
