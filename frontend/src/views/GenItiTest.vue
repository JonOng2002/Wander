<template>
  <div class="generated-itinerary">
    <div v-if="loading" class="empty-message">Loading itinerary...</div>
    <div v-else-if="!itinerary" class="empty-message">
      <h2>No itinerary generated. Please add places to generate an itinerary.</h2>
    </div>
    <div v-else class="main-content row g-0">
      <!-- Left Side: Itinerary Details -->
      <div class="col-md-6 col-12 itinerary-details">
        <h2>{{ itinerary.itinerary_summary }}</h2>
        <p>{{ getNumDays }} days</p>
        <div v-for="(day, index) in itinerary.day_by_day_itineraries" :key="index" class="itinerary-row">
          <h4>Day {{ day.day }} - {{ day.date }}</h4>
          <h5>{{day.summary}}</h5>
          <ul>
            <li v-for="(activity, actIndex) in day.activities" :key="actIndex">
              <div>{{ activity.photo_url }}</div>
              <!-- how to display activity image via google places api -->
              <strong>{{ activity.time }}:</strong> {{ activity.activity_name }} <br>
              <em>Location:</em> {{ activity.location?.name || 'Unknown location' }} <br>
            </li>
          </ul>
        </div>
      </div>

      <!-- Right Side: Google Maps -->
      <div class="col-md-6 col-12 map-container">
        <GoogleMap
          v-if="isMapReady" 
          :api-promise="apiPromise"
          :center="mapCenter"
          :zoom="15"
          style="width: 100%; height: 100%"
        >
        <CustomMarker
            v-for="(activity, index) in allActivities"
            :key="index"
            :options="{ position: { lat: activity.location?.coordinates?.latitude || 0, lng: activity.location?.coordinates?.longitude || 0 }, anchorPoint: 'BOTTOM_CENTER' }"
          >
          <div style="text-align: center">
              <div>{{ activity.location?.name }}</div>
              <img src="https://i.postimg.cc/8zLP2XNf/Image-16-10-24-at-2-27-PM.jpg" width="50" height="50" style="margin-top: 8px" />
            </div>
          </CustomMarker>
        </GoogleMap>
        <div v-else>Loading map...</div> <!-- Show loading state for map -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import router from '@/router';
import { inject } from 'vue';
import { GoogleMap, CustomMarker } from 'vue3-google-map'; // Import GoogleMap and Marker

// Inject the globally provided apiPromise
const apiPromise = inject('apiPromise');

// Reactive properties to hold data
const itinerary = ref(null);
const loading = ref(false);
const errorMessage = ref(null);
const isMapReady = ref(false); // Track when map is ready
const mapCenter = ref({ lat: 0, lng: 0 }); // The center of the map
const allActivities = ref([]); // Hold all activities for markers on the map
const { start, end, tripType, countryCode, itinerary: itineraryData, selectedTags } = router.currentRoute.value.query;
console.log('query:', start, end, tripType, countryCode, itineraryData, selectedTags);

// Calculate the number of days in the itinerary
const getNumDays = computed(() => {
  return itinerary.value ? itinerary.value.day_by_day_itineraries.length : 0;
});

// Fetch itinerary data from the backend (Flask)
const submitData = async () => {

  // Safely parse itinerary and selected tags if they exist
  const parsedItinerary = itineraryData ? JSON.parse(itineraryData) : [];
  const parsedTags = selectedTags ? JSON.parse(selectedTags) : [];

  const dataToSend = {
    startDate: start,
    endDate: end,
    tripType,
    countryCode,
    itinerary: parsedItinerary, // Parsed or empty array
    tags: parsedTags, // Parsed or empty array
  };

  // Set loading state
  loading.value = true;
  errorMessage.value = null;

  try {
    // Send a POST request to the backend to fetch the generated itinerary
    const response = await axios.post("http://127.0.0.1:5000/generate-itinerary", dataToSend, {
      headers: {
        "Content-Type": "application/json",
      },
    });

    // Update the itinerary and activities
    itinerary.value = response.data;
    allActivities.value = itinerary.value.day_by_day_itineraries.flatMap(day => day.activities);

    // Set the map center to the first available activity's location
    const firstActivity = allActivities.value.find(activity => activity.location?.coordinates);
    if (firstActivity && firstActivity.location.coordinates) {
      mapCenter.value = {
        lat: firstActivity.location.coordinates.latitude,
        lng: firstActivity.location.coordinates.longitude,
      };
    }

    // Once the itinerary is fetched, check if the API is ready
    const google = await apiPromise;
    if (google && google.maps) {
      isMapReady.value = true; // Set the map as ready once the API is available
    }
  } catch (error) {
    // Handle errors
    errorMessage.value = 'Failed to generate itinerary.';
    console.error(error);
  } finally {
    // Stop the loading state
    loading.value = false;
  }
};

// Fetch itinerary data when the component is mounted
onMounted(() => {
  submitData();
});
</script>

<style scoped>
/* General styling */
h2 {
  font-family: 'Cormorant Garamond', serif;
  font-weight: bolder;
}

.generated-itinerary h2 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 3rem;
  font-weight: bold;
}

.no-itinerary-message {
  text-align: center;
  font-size: 1.2rem;
  color: grey;
  margin-top: 20px;
}

.date-column p {
  font-family: 'Roboto', sans-serif;
  font-size: 1.2rem;
  color: #333;
}

.main-content {
  display: flex;
  height: 100vh;
}

.generated-itinerary {
  font-family: "Roboto", sans-serif;
  margin: 0;
  padding: 0;
}

.itinerary-details {
  height: 100vh;
  overflow-y: scroll;
  padding: 20px;
}

.itinerary-details::-webkit-scrollbar {
  display: none;
}

.map-container {
  background-color: #F8F9FA;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

.map {
  width: 100%;
  height: 100%;
}

@media (max-width: 768px) {
  .map-container {
    display: none;
  }
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-radius: 50%;
  border-top: 4px solid #4caf50;
  width: 30px;
  height: 30px;
  animation: spin 2s linear infinite;
}

.error-message {
  color: red;
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 10px;
}

button:hover {
  background-color: #45a049;
}
</style>