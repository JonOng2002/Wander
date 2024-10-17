import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '@/views/MainPage.vue';
import UploadVideo from '@/components/UploadVideo.vue';
import AnalyseLink from '@/components/AnalyseLink.vue';
import ProfilePage from '@/views/ProfilePage.vue'; 
import SavedPlaces from '@/views/SavedPlaces.vue';
import GeneratedItinerary from '@/views/GeneratedItinerary.vue';
import MyDestinations from '@/views/MyDestinations.vue';
import DestinationDetails from '@/views/DestinationDetails.vue';


const routes = [
  {
    path: '/', // Root path loads MainPage
    name: 'MainPage',
    component: MainPage, 
  },  
  {
    path: '/mainpage',
    name: 'MainPageAlias',
    component: MainPage,
  },
  {
    path: '/upload',
    name: 'UploadVideo',
    component: UploadVideo,
  },
  {
    path: '/analyze',
    name: 'AnalyseLink',
    component: AnalyseLink,
  },
  {
    path: '/profile',
    name: 'ProfilePage',
    component: ProfilePage,
  },
  {
    path: '/savedplaces',
    name: 'SavedPlaces',
    component: SavedPlaces,
  },
  {
    path: '/generated',
    name: 'GeneratedItinerary',
    component: GeneratedItinerary, 
  },
  {
    path: '/destinations',
    name: 'MyDestinations',
    component: MyDestinations,
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
