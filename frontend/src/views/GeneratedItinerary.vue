<template>
  <div class="generated-itinerary">
    <AppNavbar class="sticky-top"></AppNavbar>

    <!-- If Loading / generatedItinerary is empty -->
    <div v-if="loading" class="empty-message">Loading itinerary...</div>
    <div v-else-if="!itinerary" class="empty-message">
      <div class="row justify-content-between align-items-center sticky-header g-0">
        <div class="col-3 date-column">
          <h2>My Itineraries</h2>
        </div>
      </div>
      <div class="no-itinerary-message">
        <p>No itinerary generated. Please <router-link to="/savedPlaces">add places</router-link> to generate an itinerary.</p>
      </div>
    </div>

    <!-- When Itinerary exists -->
    <div v-else class="main-content row g-0">
      <!-- Left Side: Itinerary Details -->
      <div class="col-md-6 col-12 itinerary-details">
        <div class="row justify-content-between align-items-center g-0">
          <div class="col-12 date-column">
            <p>Review our recommendations</p>
            <h2>Personalized itinerary for <strong>{{ userName }}</strong></h2> <!-- User's name -->
            <p>{{ country }} • {{ getNumDays }} days</p> <!-- Country and number of days -->
          </div>
        </div>

        <!-- Loop through itinerary days -->
        <div v-for="(day, index) in itinerary.day_by_day_itineraries" :key="index" class="day-section">
          <div class="day-header">Day {{ day.day }} : {{ day.date }}</div>
          <div class="day-description">{{ day.summary }}</div>

          <div class="itinerary-table">
            <!-- Loop through activities -->
            <div class="itinerary-row" v-for="(activity, actIndex) in day.activities" :key="actIndex">
              <div class="time-column">{{ activity.time }}</div>
              <div class="place-column">
                <h5>{{ activity.activity_name }}</h5>
                <p><em>Location:</em> {{ activity.location?.name || 'Unknown location' }}</p>

                <!-- Show activity image if available -->
                <div v-if="activity.location.photo_url">
                  <img :src="activity.location.photo_url" class="place-image" :alt="activity.activity_name" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Save to My Itineraries Button -->
        <button @click="saveToItinerary" class="btn save-itinerary-button">Save to My Itineraries</button>
      </div>

      <!-- Right Side: Google Maps -->
      <div class="col-md-6 col-12 map-container">
        <div id="location-map" class="map">
          <GoogleMap v-if="isMapReady" :api-promise="apiPromise" :center="mapCenter" :zoom="15" style="width: 100%; height: 100%">
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

    <!-- Popup for confirmation -->
    <div v-if="showPopup" class="popup">
      <p>Itinerary saved successfully!</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import router from '@/router';
import { inject } from 'vue';
import { GoogleMap, CustomMarker } from 'vue3-google-map';
import { getAuth } from 'firebase/auth';
import { doc, updateDoc, arrayUnion } from 'firebase/firestore';
import { db } from '@/main';

// Inject the globally provided apiPromise
const apiPromise = inject('apiPromise');

// Reactive properties to hold data
const userName = ref(''); 
const itinerary = ref(null);
const loading = ref(false);
const errorMessage = ref(null);
const isMapReady = ref(false); // Track when map is ready
const mapCenter = ref({ lat: 0, lng: 0 }); // The center of the map
const allActivities = ref([]); // Hold all activities for markers on the map
const { start, end, tripType, countryCode, itinerary: itineraryData, selectedTags } = router.currentRoute.value.query;
const country = ref('');  // Country name
const showPopup = ref(false);  // To display confirmation

// Fetch user name from Firebase
const fetchUserName = () => {
  const auth = getAuth();
  const user = auth.currentUser;

  if (user) {
    userName.value = user.displayName || "Guest";
    console.log('User name:', userName.value);
  } else {
    console.error("User not authenticated");
  }
};

// Calculate the number of days in the itinerary
const getNumDays = computed(() => {
  const numDays = itinerary.value ? itinerary.value.day_by_day_itineraries.length : 0;
  console.log('Number of days in itinerary:', numDays);
  return numDays;
});

// Fetch itinerary data from the backend
const submitData = async () => {
  const parsedItinerary = itineraryData ? JSON.parse(itineraryData) : [];
  const parsedTags = selectedTags ? JSON.parse(selectedTags) : [];

  const dataToSend = {
    startDate: start,
    endDate: end,
    tripType,
    countryCode,
    itinerary: parsedItinerary,
    tags: parsedTags,
  };

  loading.value = true;
  errorMessage.value = null;

  try {
    const response = await axios.post("http://127.0.0.1:5000/generate-itinerary", dataToSend, {
      headers: { "Content-Type": "application/json" },
    });

    itinerary.value = response.data;
    allActivities.value = itinerary.value.day_by_day_itineraries.flatMap(day => day.activities);

    const firstActivityWithCoordinates = allActivities.value.find(activity => activity.location?.coordinates);
    if (firstActivityWithCoordinates && firstActivityWithCoordinates.location.coordinates) {
      mapCenter.value = {
        lat: firstActivityWithCoordinates.location.coordinates.latitude,
        lng: firstActivityWithCoordinates.location.coordinates.longitude,
      };
      console.log('Map center set to:', mapCenter.value);
    }

    const activityWithCity = allActivities.value.find(activity => activity.location?.city);
    country.value = activityWithCity?.location?.city || "Unknown Location";
    console.log('Country (city) set to:', country.value);

    const google = await apiPromise;
    if (google && google.maps) {
      isMapReady.value = true;
      console.log('Google Maps API is ready');
    }
  } catch (error) {
    errorMessage.value = 'Failed to generate itinerary.';
    console.error('Error generating itinerary:', error);
  } finally {
    loading.value = false;
  }
};

const saveToItinerary = async () => {
  const auth = getAuth();
  const user = auth.currentUser;

  if (user) {
    const userRef = doc(db, "users", user.uid);

    // Create the object to save
    const itineraryToSave = {
      itinerary: itinerary.value,  // Full itinerary response from backend
      country: country.value,      // Store country or city info
      createdAt: new Date(),       // Metadata: when this itinerary was created
    };

    // Log the data to be saved
    console.log("Itinerary to save:", itineraryToSave);

    try {
      // Save the itinerary in Firestore
      await updateDoc(userRef, {
        savedItineraries: arrayUnion(itineraryToSave),
      });

      // Show popup on successful save
      showPopup.value = true;
      setTimeout(() => (showPopup.value = false), 3000);
      console.log("Itinerary saved successfully.");
    } catch (error) {
      console.error("Error saving itinerary:", error);
    }
  } else {
    console.error("User not authenticated");
  }
};

onMounted(() => {
  fetchUserName();
  submitData();
});
</script>

<style scoped>
/* General styling */
h2 {
  font-family: 'Cormorant Garamond', serif;
  font-weight: bolder;
}

/* For the main destination title */
.generated-itinerary h2 {
  font-family: 'Cormorant Garamond', serif; /* Update font style */
  font-size: 3rem; /* Larger font size for the destination */
  font-weight: bold; /* Ensure boldness */
}

.no-itinerary-message {
  text-align: center;
  font-size: 1.2rem;
  color: grey;
  margin-top: 20px;
}

/* For the subtext under the main title */
.date-column p {
  font-family: 'Roboto', sans-serif; /* Update font style */
  font-size: 1.2rem; /* Adjust font size */
  color: #333; /* Darker color for the date information */
}

/* Main Layout */
.main-content {
  display: flex;
  height: 100vh;
}

.generated-itinerary {
  font-family: "Roboto", sans-serif;
  margin: 0;
  padding: 0;
}

.sticky-top {
  top: 0;
  position: sticky;
  z-index: 1020; /* Higher z-index to ensure navbar stays above other elements */
  background-color: black; /* Ensure the background remains black */
}

.sticky-header {
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 1000;
  padding: 10px 5%;
  border-bottom: 1px solid lightgrey;
}

.date-column {
  text-align: left;
  padding-left: 15px;
  font-family: 'Roboto', sans-serif;
  font-size: 1.5rem;
  margin-top: 10px;
  margin-bottom: 10px;
}

.itinerary-details {
  height: 100vh;
  overflow-y: scroll;
  padding: 20px;
}

/* Remove the inner scrollbar */
.itinerary-details::-webkit-scrollbar {
  display: none;
}

/* Day Section Styling */
.day-section {
  margin-bottom: 20px;
  background-color: #fdfdfd;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.day-header {
  font-weight: bold;
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.day-description {
  margin-bottom: 20px;
  color: #666;
}

/* Table Styling */
.itinerary-table {
  display: grid;
  grid-template-columns: 1fr 3fr;
  gap: 10px;
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 10px;
}

.itinerary-row {
  display: contents; /* Each row with time and place */
}

.time-column {
  text-align: left;
  font-weight: bold;
  padding: 10px 0;
}

.place-column {
  padding: 10px 0;
}

.place-column h5 {
  font-size: 1.2rem;
  margin: 0;
}

.place-column img {
  max-width: 150px;
  border-radius: 8px;
}

/* Map Styling */
.map-container {
  background-color: #F8F9FA;
  height: 100vh;
  position: relative;
  overflow: hidden; /* Prevent scrolling in the map */
}

.map {
  width: 100%;
  height: 100%;
}

.save-itinerary-button {
  background-color: #007bff;
  color: white;
  padding: 10px;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.save-itinerary-button:hover {
  background-color: #0056b3;
}

.popup {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: green;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  opacity: 1;
  transition: opacity 0.3s ease;
}

@media (max-width: 768px) {
  /* Hide Map at Smaller Screens */
  .map-container {
    display: none;
  }
}
</style>