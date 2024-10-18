<template>
  <div id="app">
    <div class="header" v-if="!isAuthPage">
      <!-- Include the Navbar component conditionally -->
      <AppNavbar />
    </div>

    <div class="router-container">
      <router-view></router-view> 
    </div><!-- This is where the matched component will be rendered -->
  </div>
</template>

<script>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import AppNavbar from './components/AppNavbar.vue';

export default {
  name: 'App',
  components: {
    AppNavbar, // Register the Navbar component
  },
  setup() {
    const route = useRoute();

    // Check if the current route is sign-in or login
    const isAuthPage = computed(() => {
      return route.name === 'SignIn' || route.name === 'LogIn';
    });

    return {
      isAuthPage,
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
  position: sticky; /* Ensures it sticks to the top */
  top: 0;
  z-index: 1000;
  background-color: white; /* Ensure a solid background for the navbar */
}
#app {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 0px;
  margin: 0;
}

.header {
  display: flex;
  align-items: center;
  width: 100%;
}

.router-container {
  width: 100%;
  margin: 0;
  padding: 0;
}
</style>
