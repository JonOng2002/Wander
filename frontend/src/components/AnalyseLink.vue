<template>
  <div id="app">
    <!-- Navigation Bar (Always Visible) -->
    <nav>
      <h1>Wander</h1>
    </nav>
    
    <!-- Conditional Display: Only show if `showQueryScreen` is true -->
    <div v-if="showQueryScreen">
      <!-- Input field for the TikTok link -->
      <input v-model="tiktokLink" placeholder="Paste TikTok link here" />
      <button @click="analyse">Find out the place!</button>
      
      <!-- Loading bar --> 
      <LoadingBar :isLoading="isLoading" />
    </div>
      <!-- Error Message -->
      <div v-if="errorMessage">{{ errorMessage }}</div>
  </div>
</template>

<script>
import axios from 'axios';
import LoadingBar from './LoadingBar.vue';

export default {
  components: {
    LoadingBar,
  },
  data() {
    return {
      tiktokLink: '', // To store the user's input (TikTok link)
      videoInfo: null, // To store the video info
      relatedPlaces: [], // To store the related places
      errorMessage: '', // To store any error messages
      isLoading: false, // Loading state for showing the loading bar
      showQueryScreen: true // Determines whether to show the input screen or results
    };
  },
  methods: {
    isValidUrl(url) {
      const regex = /^(https?:\/\/)?(www\.)?(tiktok\.com\/(@[\w.-]+\/video\/\d+)|(vt\.tiktok\.com\/[\w\d]+)).*$/;
      return regex.test(url);
    },
  // Function to fetch video info and related places from the backend
  async analyse() {
    if (this.isValidUrl(this.tiktokLink)) {
      this.isLoading = true; // Show the loading bar
      this.errorMessage = ''; // Clear any previous error messages
      this.videoInfo = null; // Clear any previous video info
      this.relatedPlaces = []; // Clear any previous related places
      
      console.log('Analyzing TikTok link:', this.tiktokLink);
      try {
        // Make an API call to the Flask backend with the TikTok link as a param
        const response = await axios.get(`http://127.0.0.1:5000/video-info-comments`, {
          params: {
            url: this.tiktokLink, // Pass the TikTok link directly
            withCredentials: true,
          },
        });

        console.log("Backend response:", response.data);

          // Directly assign the openai_response object, no need to JSON.parse
          const data = response.data.openai_response;

          // Set video info and related places
          this.videoInfo = data.video_info;
          this.locationInfo = data.location_info;
          this.relatedPlaces = data.related_places;

          // Navigate to SearchedLocation component and pass the data as route params
          this.$router.push({
            path: '/location',
            query: {
              videoInfo: JSON.stringify(this.videoInfo),
              locationInfo: JSON.stringify(this.locationInfo),
              relatedPlaces: JSON.stringify(this.relatedPlaces)
            }
          });

      } catch (error) {
        console.error(error);
        this.handleError(error); // Handle the error
      } finally {
        this.isLoading = false; // Hide the loading bar
      }
    } else {
      this.errorMessage = 'Invalid TikTok link. Please check and try again.'; // Handle invalid TikTok links
    }
  },

  handleError(error) {
    if (error.response && error.response.status === 500) {
      this.errorMessage = 'Server error. Please try again later.';
    } else if (error.message === 'Network Error') {
      this.errorMessage = 'Network issue! Please check your connection.';
    } else {
      this.errorMessage = 'An unexpected error occurred. Please try again.';
    }
  }
}
};
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 60px;
}

input {
  padding: 10px;
  margin-right: 10px;
}

button {
  padding: 10px;
}

nav {
  background-color: #333;
  color: white;
  padding: 1rem;
}
</style>