import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '@/views/MainPage.vue';
import UploadVideo from '@/components/UploadVideo.vue';
import AnalyseLink from '@/components/AnalyseLink.vue';
import ProfilePage from '@/views/ProfilePage.vue'; 
import SavedPlaces from '@/views/SavedPlaces.vue';
import GeneratedItinerary from '@/views/GeneratedItinerary.vue';
import MyDestinations from '@/views/MyDestinations.vue';
import DestinationDetails from '@/views/DestinationDetails.vue';
import TestItinerary from '@/views/TestItinerary.vue';
import { getAuth, onAuthStateChanged } from 'firebase/auth';

const routes = [

  { path: '/', name: 'MainPage', component: MainPage },  
  { path: '/about', name: 'AboutPage', component: AboutPage },
  { path: '/location', name: 'ExtractedLocation', component: ExtractedLocation },
  { path: '/savedplaces', name: 'SavedPlaces', component: SavedPlaces },
  { path: '/about', name: 'About', component: AboutPage },
  { path: '/log-in', name:'LogIn', component: LogIn }, // Updated to use LogIn
  { path: '/profile', name: 'ProfilePage', component: ProfilePage },
  { path: '/itinerary', name: 'GeneratedItinerary', component: GeneratedItinerary },
  { path: '/sign-up', name: 'SignUp', component: SignUp },
  { path: '/destinations', name: 'MyDestinations', component: MyDestinations },
  { path: '/test-itinerary', name: 'TestItinerary', 
    component: TestItinerary,
    props: (route) => ({
    itineraryGenerated: route.query.itineraryGenerated === 'true',
    itinerary: route.query.itinerary ? JSON.parse(route.query.itinerary) : []
  })
  },
  {
    path: '/country/:country', // Ensure the param is named 'country'
    name: 'DestinationDetails',
    component: DestinationDetails,
    props: true, // Pass route params as props to the component
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
