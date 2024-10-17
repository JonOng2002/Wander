<template>
  <div>
    <!-- Location Information -->
    <div v-if="locationInfo">
      <h3>Fetched location</h3>
      <p><strong>Place:</strong> {{ locationInfo.place_name }}</p>
      <p><strong>Country:</strong> {{ locationInfo.country }}</p>
      <p><strong>City:</strong> {{ locationInfo.city }}</p>
      <p><strong>Activities:</strong> {{ locationInfo.activities?.join(', ') || 'No activities available' }}</p>
      <p><strong>Summary:</strong> {{ locationInfo.summary || 'No summary available' }}</p>
      <p><strong>Latitude:</strong> {{ locationInfo.coordinates.latitude }}</p>
      <p><strong>Longitude:</strong> {{ locationInfo.coordinates.longitude }}</p>
      <img 
        :src="locationInfo.place_png" 
        @error="handleImageError" 
        alt="Image of {{ locationInfo.place_name }}" 
        width="300px"
      />

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
        :activities="locationInfo.activities" 
        :summary="locationInfo.summary"
      ></save-place-button>
    </div>

    <!-- Related Places Section -->
    <div v-if="relatedPlaces.length">
      <h2>Related Places:</h2>
      <ul>
        <li v-for="place in relatedPlaces" :key="place.place_name">
          <strong>Place:</strong> {{ place.place_name }}<br />
          <strong>Country:</strong> {{ place.country }} <br />
          <strong>City:</strong> {{ place.city }} <br />
          <strong>Coordinates:</strong> ({{ place.coordinates.latitude }}, {{ place.coordinates.longitude }}) <br />
          <strong>Activities:</strong> {{ place.activities?.join(', ') || 'No activities available' }} <br />
          <strong>Summary:</strong> {{ place.summary || 'No summary available' }} <br />
          <img 
            :src="place.place_png" 
            @error="handleImageError" 
            alt="Image of {{ place.place_name }}" 
            width="300px" 
          />

          <!-- Save button for each related place -->
          <save-place-button 
            :placeName="place.place_name" 
            :country="place.country"
            :city="place.city"
            :latitude="place.coordinates.latitude"
            :longitude="place.coordinates.longitude"
            :placePng="place.place_png"
            :userId="userId"
            :activities="place.activities"
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

// Function to format location data
const formatLocation = (location) => {
  return {
    place_name: location?.place_name || "Unknown Place",
    country: location?.country || "Unknown Country",
    city: location?.city || "Unknown City",
    coordinates: {
      latitude: location?.coordinates?.latitude || 0,
      longitude: location?.coordinates?.longitude || 0,
    },
    place_png: location?.place_png || "/default-image.png", // Fallback if no image
    summary: location?.location_summary || "No summary available", // Use location_summary for summary
    activities: location?.activities || [], // Make sure to include activities
  };
};

const loader = new Loader({
  apiKey: 'AIzaSyDd5eMLnn0oB1z4JqV3QWgRhFWYJ1PFI0k', // Replace with your actual API key
  version: 'weekly',
  libraries: ['places'], // You can include more libraries if needed
});

// Load the Google Maps API and create the apiPromise
const apiPromise = loader.load();

// Retrieve video and location data from query params
onMounted(() => {
  if (route.query.locationInfo) {
    locationInfo.value = formatLocation(JSON.parse(route.query.locationInfo)); // Format location data

    // Set map center based on the location coordinates
    if (locationInfo.value.coordinates.latitude && locationInfo.value.coordinates.longitude) {
      center.value = {
        lat: locationInfo.value.coordinates.latitude,
        lng: locationInfo.value.coordinates.longitude,
      };
    }
  }
  if (route.query.relatedPlaces) {
    relatedPlaces.value = JSON.parse(route.query.relatedPlaces).map((place) =>
      formatLocation(place)
    ); // Standardize related places
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

// Function to handle image error
const handleImageError = (event) => {
  event.target.src = 'https://i.postimg.cc/8zLP2XNf/Image-16-10-24-at-2-27-PM.jpg'; // Set the src to the alternative image URL
};
</script>

<style scoped>
/* Add styles if needed */
</style>