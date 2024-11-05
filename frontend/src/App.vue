<template>
  <div id="app">
    <!-- Navbar appears only when not in auth, itinerary details, or generated itinerary pages -->
    <div class="header" v-if="!isExcludedPageNav">
      <AppNavbar />
    </div>


    <div class="router-container">
      <router-view></router-view>
    </div>

    <!-- Footer Component -->
    <div v-if="!isExcludedPageFooter">
      <AppFooter />
    </div>
    
  </div>
</template>

<script>
import AppNavbar from './components/AppNavbar.vue';
import AppFooter from './components/AppFooter.vue';
import { computed } from 'vue';
import { useRoute } from 'vue-router';


export default {
  name: 'App',
  components: {
    AppNavbar,
    AppFooter,
  },
  setup() {
    const route = useRoute();

    // Consolidated check to see if the current route is one of the pages where the navbar should be hidden
    const isExcludedPageNav = computed(() => {
      return (
        route.name === 'SignUp' ||
        route.name === 'LogIn' ||
        route.name === 'ItineraryDetails' ||
        route.name === 'GeneratedItinerary' ||
        route.name === 'LocationDate' || 
        route.name === 'CalendarPage' || 
        route.name === 'TagsPage' ||
        route.name === 'Welcome'

      );
    });

    const isExcludedPageFooter = computed(() => {
      return (
        route.name === 'SignUp' ||
        route.name === 'LogIn' ||
        route.name === 'ItineraryDetails' ||
        route.name === 'GeneratedItinerary' ||
        route.name === 'LocationDate' || 
        route.name === 'CalendarPage' || 
        route.name === 'TagsPage' || 
        route.name === 'MainPage' || 
        route.name === 'AboutPage' || 
        route.name === 'ExtractedLocation' || 
        route.name === 'ItineraryBuilder'
      );
    });

    return {
      isExcludedPageNav,
      isExcludedPageFooter,
    };
  },

};


</script>

<style>
body {
  margin: 0;
  background-color: #f0f0f0;
}
</style>

<style scoped>
.header {
  display: flex;
  align-items: center;
  width: 100%;
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: white; /* Ensure a solid background for the navbar */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Optional shadow for depth */
  
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* Ensure the app takes up the full viewport height */
}

.router-container {
  width: 100%;
  margin: 0;
}

/* In a global stylesheet or in App.vue's <style> block */
footer {
  width: 100vw; /* Forces full viewport width */
  left: 0;
  right: 0;
}

</style>
