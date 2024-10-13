<template>
    <div class="homepage">
      <p class="searchBarTitle">Where would you like to wander?</p>

      <SearchBar @submit-link="handleLinkSubmit" />
    </div>


  </template>
  
  <script>
  import SearchBar from '@/components/SearchBar.vue'; // Import the SearchBar component
  export default {
    name: 'MainPage',
    components:{
      SearchBar, // Register the SearchBar component
    },
    methods: {
    handleLinkSubmit(link) {
      console.log('Link submitted on Home Page:', link);
      // Handle the link submitted in this specific view
    },
  },
};
  
  </script>
  
  <style scoped>
  /* Your styles here */
  .homepage {
  text-align: center;
  padding-top: 50px; /* Add some padding to ensure it's visible */
  padding: 5%;
}

.searchBarTitle {
  font-size: 3rem;
  margin-bottom: 20px;
  font-family: 'Cormorant Garamond', serif;
  font-weight: bold;
}

  </style>