<template>
  <div class="homepage">
    <p class="searchBarTitle">Where would you like to wander?</p> 

    <SearchBar :disabled="isLoading" @submit-Link="handleLinkSubmit" />

    <LoadingBar :isLoading="isLoading" v-if="isLoading"/>

    <!-- Error Message -->
    <div v-if="errorMessage">{{ errorMessage }}</div>

    <ExtractedLocations 
      v-if="extractedLocationsState.locationInfo && extractedLocationsState.relatedPlaces"
      :locationInfo="extractedLocationsState.locationInfo"
      :relatedPlaces="extractedLocationsState.relatedPlaces"
      :userId="userId"
      :savedPlaces="savedPlaces"
    />
  </div>
</template>

<script>
import SearchBar from '@/components/SearchBar.vue';
import { doc, getDoc } from "firebase/firestore"; 
import { db, auth } from "@/main";  
import { onAuthStateChanged } from 'firebase/auth'; 
import LoadingBar from '@/components/LoadingBar.vue'; 
import axios from 'axios';
import ExtractedLocations from './ExtractedLocations.vue';
import { inject } from 'vue';

export default {
  name: 'MainPage',
  components: {
    SearchBar, 
    LoadingBar,
    ExtractedLocations,
  },
  setup() {
    const extractedLocationsState = inject('extractedLocationsState'); // Inject the global state

    return { extractedLocationsState };
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
        await this.fetchUserData();
      }
    });
  },
  methods: {
    handleLinkSubmit(link) {
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
          console.log("Backend response:", data);

          if (data.error) {
            throw new Error("Error generating response from OpenAI.");
          }
        
          // Set the location info and related places in the global state
          this.extractedLocationsState.setLocationInfo(data.location_info);
          this.extractedLocationsState.setRelatedPlaces(data.related_places);
        } catch (error) {
          this.errorMessage = "Error generating response from OpenAI.";
        } finally {
          this.isLoading = false; // Stop loading
        }
      } else {
        this.errorMessage = "Invalid TikTok link. Please try again.";
      }
    },

    isValidUrl(url) {
      const regex = /^(https?:\/\/)?(www\.)?(tiktok\.com\/(@[\w.-]+\/video\/\d+)|(vt\.tiktok\.com\/[\w\d]+)).*$/;
      return regex.test(url);
    },

    async fetchUserData() {
      try {
        const userRef = doc(db, "users", this.userId);
        const userDoc = await getDoc(userRef);
        
        if (userDoc.exists()) {
          const userData = userDoc.data();
          this.savedPlaces = userData.savedPlaces || [];
          this.generatedItineraries = userData.generatedItineraries || [];
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