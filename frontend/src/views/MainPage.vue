<template>
  <div class="homepage">
    <p class="searchBarTitle">Where would you like to wander?</p> 
    
    <SearchBar :disabled="isLoading" @submit-Link="handleLinkSubmit" />

    <LoadingBar :isLoading="isLoading" />

    <!-- Displaying saved places -->
    <div v-if="savedPlaces.length > 0" class="saved-places">
      <h3>Saved Places</h3>
      <ul>
        <li v-for="place in savedPlaces" :key="place.name">
          <strong>{{ place.name }}</strong> - {{ place.location }}: {{ place.description }}
        </li>
      </ul>
    </div>

    <!-- Displaying generated itineraries -->
    <div v-if="generatedItineraries.length > 0" class="generated-itineraries">
      <h3>Generated Itineraries</h3>
      <ul>
        <li v-for="itinerary in generatedItineraries" :key="itinerary.destination">
          <strong>{{ itinerary.destination }}</strong> - {{ itinerary.duration }}:
          <ul>
            <li v-for="activity in itinerary.activities" :key="activity">{{ activity }}</li>
          </ul>
        </li>
      </ul>
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage">{{ errorMessage }}</div>

    <!-- Loading bar, Yet to be styled -->
    <LoadingBar v-if="isLoading" />
  </div>
</template>

<script>
import SearchBar from '@/components/SearchBar.vue';
import { doc, getDoc } from "firebase/firestore"; 
import { db, auth } from "@/main";  
import { onAuthStateChanged } from 'firebase/auth'; 
import LoadingBar from '@/components/LoadingBar.vue'; 

import axios from 'axios';

export default {
  name: 'MainPage',
  components: {
    SearchBar, 
    LoadingBar 
  },
  data() {
    return {
      userId: null, 
      savedPlaces: [],
      generatedItineraries: [],
      errorMessage: "",
      isLoading: false,
      tiktokLink: "", // Add tiktokLink to hold the link
    };
  },
  mounted() {
    onAuthStateChanged(auth, async (user) => {
      if (user) {
        this.userId = user.uid;
        console.log("User ID:", this.userId);
        await this.fetchUserData();
      } else {
        console.log("No user is signed in.");
      }
    });
  },
  methods: {
    handleLinkSubmit(link) {
      console.log('Link submitted on Home Page:', link);
      this.tiktokLink = link; // Update the tiktokLink with the submitted link
      this.analyse(); // Call the analyse function with the link
    },

    async analyse() {
      if (this.isValidUrl(this.tiktokLink)) {
        this.isLoading = true; // Start loading
        this.errorMessage = ""; // Clear error messages
        try {
          const response = await axios.get(`http://127.0.0.1:5000/video-info-comments`, {
            params: {
              url: this.tiktokLink,
              withCredentials: true,
            },
          });

          const data = response.data.openai_response;

          if (data.error) {
            throw new Error("Error generating response from OpenAI.");
          }
          
          const videoInfo = data.video_info;
          const relatedPlaces = data.related_places;

          // Redirect to the SearchedLocation component with query params
          this.$router.push({
            path: "/location",
            query: {
              videoInfo: JSON.stringify(videoInfo),
              locationInfo: JSON.stringify(data.location_info),
              relatedPlaces: JSON.stringify(relatedPlaces),
            },
          });
        } catch (error) {
          console.error(error);
          this.errorMessage = "Error generating response from OpenAI.";
        } finally {
          this.isLoading = false; // Stop loading
        }
      } else {
        this.errorMessage = "Invalid TikTok link. Please try again.";
      }
    },

    isValidUrl(url) {
      const regex =
        /^(https?:\/\/)?(www\.)?(tiktok\.com\/(@[\w.-]+\/video\/\d+)|(vt\.tiktok\.com\/[\w\d]+)).*$/;
      return regex.test(url);
    },

    async fetchUserData() { //need revisit this code again becaue change in the firebase from jiaxin's one to jon's.
      try {
        const userRef = doc(db, "users", this.userId);
        const userDoc = await getDoc(userRef);
        
        if (userDoc.exists()) {
          const userData = userDoc.data();
          this.savedPlaces = userData.savedPlaces || [];
          this.generatedItineraries = userData.generatedItineraries || [];
          console.log("User data fetched successfully:", userData);
        } else {
          console.log("No user data found.");
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    }
  }
};
</script>

<style scoped>
.homepage {
  text-align: center;
  padding-top: 50px;
  padding: 5%;
}

.searchBarTitle {
  font-size: 3rem;
  margin-bottom: 20px;
  font-family: 'Cormorant Garamond', serif;
  font-weight: bold;
}

.saved-places, .generated-itineraries {
  margin-top: 40px;
}

.saved-places ul, .generated-itineraries ul {
  list-style-type: none;
  padding: 0;
}

.saved-places li, .generated-itineraries li {
  margin: 10px 0;
}
</style>