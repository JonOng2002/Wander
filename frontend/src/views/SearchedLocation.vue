<template>
  <div v-if="videoInfo">
    <h2>Video Information</h2>
    <p><strong>Title:</strong> {{ videoInfo.title }}</p>
    <p><strong>Author:</strong> {{ videoInfo.author }}</p>
    <p><strong>Play Count:</strong> {{ videoInfo.play_count }}</p>
    <p><strong>Likes:</strong> {{ videoInfo.likes }}</p>
    <p><strong>Comments Count:</strong> {{ videoInfo.comments_count }}</p>
  </div>
  
  <!-- Standardized Location Information from the video -->
  <div v-if="locationInfo">
    <h3>Location Information</h3>
    <p><strong>Place:</strong> {{ locationInfo.place_name }}</p>
    <p><strong>Country:</strong> {{ locationInfo.country }}</p>
    <p><strong>City:</strong> {{ locationInfo.city }}</p>
    <p><strong>Latitude:</strong> {{ locationInfo.coordinates.latitude }}</p>
    <p><strong>Longitude:</strong> {{ locationInfo.coordinates.longitude }}</p>
    <img :src="locationInfo.place_png" alt="Image of {{ locationInfo.place_name }}" width="300px"/>
    
    <!-- Save location of the video -->
    <save-place-button 
      :placeName="locationInfo.place_name" 
      :country="locationInfo.country"
      :city="locationInfo.city"
      :latitude="locationInfo.coordinates.latitude"
      :longitude="locationInfo.coordinates.longitude"
      :placePng="locationInfo.place_png"
      :userId="userId" 
    ></save-place-button>
  </div>

  <!-- Standardized Related Places -->
  <div v-if="relatedPlaces.length">
    <h2>Related Places:</h2>
    <ul>
      <li v-for="place in relatedPlaces" :key="place.place_name">
        <strong>{{ place.place_name }}</strong>
        
        <!-- Handle cases where activities may be undefined -->
        <div v-if="place.activities && place.activities.length">
          - {{ place.activities.join(', ') }}
        </div>
        <div v-else>
          No activities available
        </div>
        
        <strong>Country:</strong> {{ place.country }} <br/>
        <strong>City:</strong> {{ place.city }} <br/>
        <strong>Coordinates:</strong> ({{ place.coordinates.latitude }}, {{ place.coordinates.longitude }}) <br/>
        <img :src="place.place_png" alt="Image of {{ place.place_name }}" width="300px"/>
        
        <!-- Save button for each related place -->
        <save-place-button 
          :placeName="place.place_name" 
          :country="place.country"
          :city="place.city"
          :latitude="place.coordinates.latitude"
          :longitude="place.coordinates.longitude"
          :placePng="place.place_png"
          :userId="userId" 
        ></save-place-button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router'; 
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import SavePlaceButton from '@/components/SavePlaceButton.vue';

// Reactive state variables
const videoInfo = ref(null);
const relatedPlaces = ref([]);
const locationInfo = ref(null);
const userId = ref(null);

const route = useRoute(); 

// Function to format location data (if needed)
const formatLocation = (location) => {
  return {
    place_name: location.place_name || "Unknown Place",
    country: location.country || "Unknown Country",
    city: location.city || "Unknown City",
    coordinates: {
      latitude: location.coordinates?.latitude || 0,
      longitude: location.coordinates?.longitude || 0
    },
    place_png: location.place_png || "/default-image.png" // Fallback if no image
  };
};

// Retrieve video and location data from query params
onMounted(() => {
  if (route.query.videoInfo) {
    videoInfo.value = JSON.parse(route.query.videoInfo);
  }
  if (route.query.locationInfo) {
    locationInfo.value = formatLocation(JSON.parse(route.query.locationInfo)); // Format location data
  }
  if (route.query.relatedPlaces) {
    relatedPlaces.value = JSON.parse(route.query.relatedPlaces).map(place => formatLocation(place)); // Standardize related places
  }

  // Retrieve user ID from Firebase Authentication
  const auth = getAuth();
  onAuthStateChanged(auth, (user) => {
    if (user) {
      userId.value = user.uid; // Set the userId when authenticated
    } else {
      console.error("No user is logged in");
    }
  });
});
</script>

<style scoped>
/* Add styles if needed */
</style>