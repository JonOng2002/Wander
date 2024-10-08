import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '@/views/MainPage.vue';
import UploadVideo from '@/components/UploadVideo.vue';
import AnalyseLink from '@/components/AnalyseLink.vue';
import ProfilePage from '@/views/ProfilePage.vue'; 
import ItineraryPage from '@/views/ItineraryPage.vue';
import GeneratedItinerary from '@/views/GeneratedItinerary.vue';

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
    path: '/itinerary',
    name: 'ItineraryPage',
    component: ItineraryPage,
  },
  {
    path: '/generated',
    name: 'GeneratedItinerary',
    component: GeneratedItinerary,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
