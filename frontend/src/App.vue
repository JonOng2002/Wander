<template>
  <div id="app">
    <!-- Navbar appears only when not in auth, itinerary details, or generated itinerary pages -->
    <div class="header" v-if="!isExcludedPage">
      <AppNavbar />
    </div>


    <div class="router-container">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import AppNavbar from './components/AppNavbar.vue';
import { computed } from 'vue';
import { useRoute } from 'vue-router';


export default {
  name: 'App',
  components: {
    AppNavbar,
  },
  setup() {
    const route = useRoute();

    // Consolidated check to see if the current route is one of the pages where the navbar should be hidden
    const isExcludedPage = computed(() => {
      return (
        route.name === 'SignUp' ||
        route.name === 'LogIn' ||
        route.name === 'ItineraryDetails' ||
        // route.name === 'GeneratedItinerary' ||
        route.name === 'LocationDate' || 
        route.name === 'CalendarPage' || 
        route.name === 'TagsPage'
      );
    });

    return {
      isExcludedPage,
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
  align-items: flex-start;
  padding: 0px;
  margin: 0;
}

.router-container {
  width: 100%;
  margin: 0;
  padding: 0;
}
</style>
