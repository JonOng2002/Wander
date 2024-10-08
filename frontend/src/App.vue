<template>
  <div id="app">
    <div class="header">
      <!-- Include the Navbar component -->
      <AppNavbar />
    </div>

   
      <div class="router-container">
        <router-view></router-view> 
      </div><!-- This is where the matched component will be rendered -->
    
  </div>
</template>

<script>
import AppNavbar from './components/AppNavbar.vue';



export default {
  name: 'App',
  components: {
    AppNavbar, // Register the Navbar component
     // Register the SearchBar component
  },
  methods: {
    handleLinkSubmit(link) {
      console.log('Submitted link:', link);
      // Handle the submitted link here
    },
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

#title {
  font-size: 20px;
  margin: 10px;
  text-align: left;
  display: inline;
}

.router-container {
  width: 100%;
  /* display: flex;
  justify-content: center; */
  margin: 0;
  padding: 0;
}


</style>
