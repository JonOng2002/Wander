<template>
  <div>
    <!-- Location Information -->
    <div v-if="locationInfo">
      <h3>Fetched Location</h3>
      <p><strong>Place:</strong> {{ locationInfo.place_name }}</p>
      <p><strong>Country:</strong> {{ locationInfo.country }}</p>
      <p><strong>City:</strong> {{ locationInfo.city }}</p>
      <p><strong>Activities:</strong> {{ locationInfo.activities?.join(', ') || 'No activities available' }}</p>
      <p><strong>Latitude:</strong> {{ locationInfo.coordinates.latitude }}</p>
      <p><strong>Longitude:</strong> {{ locationInfo.coordinates.longitude }}</p>
      <img :src="locationInfo.place_png" alt="Image of {{ locationInfo.place_name }}" width="300px"/>

      <!-- Google Map displaying the location -->
      <GoogleMap
        :api-promise="apiPromise"
        style="width: 100%; height: 500px"
        :center="center"
        :zoom="15"
      >
        <Marker :options="{ position: center }" />
      </GoogleMap>

      <!-- Save location of the video -->
      <save-place-button 
        :placeName="locationInfo.place_name" 
        :country="locationInfo.country"
        :city="locationInfo.city"
        :latitude="locationInfo.coordinates.latitude"
        :longitude="locationInfo.coordinates.longitude"
        :placePng="locationInfo.place_png"
        :userId="userId" 
        :summary="locationInfo.summary"
      ></save-place-button>
    </div>

    <!-- Related Places Section -->
    <div v-if="relatedPlaces.length">
      <h2>Related Places:</h2>
      <ul>
        <li v-for="place in relatedPlaces" :key="place.place_name">
          <strong>{{ place.place_name }}</strong> - {{ place.activities?.join(', ') || 'No activities available' }} <br />
          <strong>Country:</strong> {{ place.country }} <br />
          <strong>City:</strong> {{ place.city }} <br />
          <strong>Coordinates:</strong> ({{ place.coordinates.latitude }}, {{ place.coordinates.longitude }}) <br />
          <strong>Activities:</strong> {{ place.activities?.join(', ') || 'No activities available' }} <br />
          <strong>Summary:</strong> {{ place.summary }} <br />
          <img :src="place.place_png" alt="Image of {{ place.place_name }}" width="300px" />

          <!-- Save button for each related place -->
          <save-place-button 
            :placeName="place.place_name" 
            :country="place.country"
            :city="place.city"
            :latitude="place.coordinates.latitude"
            :longitude="place.coordinates.longitude"
            :placePng="place.place_png"
            :userId="userId"
            :summary="place.summary"
          ></save-place-button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import SavePlaceButton from '@/components/SavePlaceButton.vue';
import { GoogleMap, Marker } from 'vue3-google-map';
import { Loader } from '@googlemaps/js-api-loader';

// Reactive state variables
const relatedPlaces = ref([]);
const locationInfo = ref(null);
const userId = ref(null);
const center = ref({ lat: 0, lng: 0 });

const route = useRoute();

const loader = new Loader({
  apiKey: 'AIzaSyDd5eMLnn0oB1z4JqV3QWgRhFWYJ1PFI0k', // Replace with your actual API key
  version: 'weekly',
  libraries: ['places'],
});

// Load the Google Maps API and create the apiPromise
const apiPromise = loader.load();

// Retrieve video and location data from query params
onMounted(() => {
  if (route.query.locationInfo) {
    locationInfo.value = JSON.parse(route.query.locationInfo); // Format location data

    // Set map center based on the location coordinates
    if (locationInfo.value.coordinates.latitude && locationInfo.value.coordinates.longitude) {
      center.value = {
        lat: locationInfo.value.coordinates.latitude,
        lng: locationInfo.value.coordinates.longitude,
      };
    }
  }
  if (route.query.relatedPlaces) {
    relatedPlaces.value = JSON.parse(route.query.relatedPlaces); // Standardize related places
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