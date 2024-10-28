<template>
  <div id="app">
    <div class="header" v-if="!isAuthPage">
      <!-- Include the Navbar component conditionally -->
      <AppNavbar />
    </div>

    <div class="router-container">
      <router-view></router-view> <!-- This is where the matched component will be rendered -->
    </div>
  </div>
</template>

<script>
import AppNavbar from './components/AppNavbar.vue';

export default {
  name: 'App',
  components: {
    AppNavbar, // Register the Navbar component
  },
  computed: {
    // Check if the current route is an auth page (e.g., SignUp or LogIn)
    isAuthPage() {
      const route = this.$route;
      return route.name === 'SignUp' || route.name === 'LogIn';
    },
  }
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
