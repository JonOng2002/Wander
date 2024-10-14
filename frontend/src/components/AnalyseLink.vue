<template>
  <div id="app">
    <!-- Navigation Bar -->
    <nav>
      <h1>Wander</h1>
    </nav>

    <!-- TikTok Analyser Input -->
    <div>
      <input v-model="tiktokLink" placeholder="Paste TikTok link here" />
      <button :disabled="isLoading" @click="analyse">
        {{ isLoading ? 'Loading...' : 'Find out the place!' }}
      </button>

      <!-- Loading bar --> 
      <LoadingBar :isLoading="isLoading" />

      <!-- Error Message -->
      <div v-if="errorMessage">{{ errorMessage }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router'; // for navigation
import LoadingBar from './LoadingBar.vue'; // Loading component

// Define reactive state variables
const tiktokLink = ref(""); // TikTok link input
const videoInfo = ref(null); // Video info from the response
const relatedPlaces = ref([]); // Related places from the response
const errorMessage = ref(""); // Error message to display
const isLoading = ref(false); // Loading state

// Get the router instance
const router = useRouter();

// Helper function to validate the TikTok link
const isValidUrl = (url) => {
  const regex =
    /^(https?:\/\/)?(www\.)?(tiktok\.com\/(@[\w.-]+\/video\/\d+)|(vt\.tiktok\.com\/[\w\d]+)).*$/;
  return regex.test(url);
};

// Function to handle the TikTok analysis
const analyse = async () => {
  if (isValidUrl(tiktokLink.value)) {
    isLoading.value = true; // Start loading
    errorMessage.value = ""; // Clear error messages
    videoInfo.value = null; // Reset video info
    relatedPlaces.value = []; // Reset related places

    try {
      const response = await axios.get(`http://127.0.0.1:5000/video-info-comments`, {
        params: {
          url: tiktokLink.value,
          withCredentials: true,
        },
      });

      const data = response.data.openai_response;

      if (data.error) {
            throw new Error("Error generating response from OpenAI.");
          }
      
      // Set video info and related places from the response
      videoInfo.value = data.video_info;
      relatedPlaces.value = data.related_places;

      // Redirect to the SearchedLocation component with query params
      router.push({
        path: "/location",
        query: {
          videoInfo: JSON.stringify(videoInfo.value),
          locationInfo: JSON.stringify(data.location_info),
          relatedPlaces: JSON.stringify(relatedPlaces.value),
        },
      });
    } catch (error) {
      console.error(error);
      errorMessage.value = "Error generating response from OpenAI.";
    } finally {
      isLoading.value = false; // Stop loading
    }
  } else {
    errorMessage.value = "Invalid TikTok link. Please try again.";
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