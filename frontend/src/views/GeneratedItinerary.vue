<template>
  <div class="generated-itinerary">
    <AppNavbar class="sticky-top"></AppNavbar>

    <!-- Show Overlay.vue when loading -->
    <Overlay v-if="loading" />

    <!-- Main Content (only displayed when loading is false) -->
    <div v-else class="content">

      <div class="main-content row g-0">
        <!-- Left Side: Itinerary Details -->
        <div class="itinerary-details-container">
          <div class="user-info">
        <h4>Review our recommendations for your trip</h4>
        <h2>Personalized itinerary for <strong>{{ userName }}</strong></h2>
        <h4>{{ country }} • {{ getNumDays }} days</h4>
      
          <button @click="saveToItinerary" class="save-itinerary-button">
              Save Itinerary
            </button>
          </div>
          <div class="itinerary-summary" v-if="itinerarySummary">
            <h3>Summary</h3>
            <p>{{ itinerarySummary }}</p>
          </div>
          <div class="itinerary-details">
            <div
              v-for="(day, index) in itinerary?.day_by_day_itineraries || []"
              :key="index"
              class="day-section"
            >
              <div class="day-header">
                Day {{ day.day }} : {{ day.date }}
              </div>
              <div class="day-description">{{ day.summary }}</div>

              <!-- Activity Grid with Two Items Per Row -->
              <div
                class="activity-grid"
                v-if="day.activities && day.activities.length"
              >
                <div
                  class="itinerary-item"
                  v-for="(activity, actIndex) in day.activities"
                  :key="actIndex"
                  @click="focusOnActivity(activity)"
                >
                  <div class="time-column">{{ activity.time }}</div>
                  <div class="place-column">
                    <h5>{{ activity.activity_name }}</h5>
                    <p>
                      <em>Location:</em>
                      {{ activity.location?.name || 'Unknown location' }}
                    </p>
                    <img
                      v-if="activity.location.photo_url"
                      :src="activity.location.photo_url"
                      class="place-image"
                      :alt="activity.activity_name"
                    />
                  </div>
                </div>
              </div>
              <p v-else>No activities available for this day.</p>
            </div>
          </div>
        </div>

        <!-- Right Side: Google Map -->
        <div class="map-container">
          <div v-if="isMapReady" id="location-map" class="map">
            <GoogleMap
              :api-promise="apiPromise"
              :center="mapCenter"
              :zoom="15"
              style="width: 100%; height: 100%"
            >
              <CustomMarker
                v-for="(activity, index) in allActivities"
                :key="index"
                :options="{
                  position: {
                    lat: activity.location?.coordinates?.latitude || 0,
                    lng: activity.location?.coordinates?.longitude || 0,
                  },
                  anchorPoint: 'BOTTOM_CENTER',
                }"
                @click="focusOnActivity(activity) "
              >
              <div
    :class="{
      'marker-selected': selectedActivity === activity,
    }"
    style="text-align: center"
  >
    <div>{{ activity.location?.name }}</div>
    <img
      src="https://i.postimg.cc/8zLP2XNf/Image-16-10-24-at-2-27-PM.jpg"
      width="50"
      height="50"
      style="margin-top: 8px"
      :class="{ 'selected-marker-image': selectedActivity === activity }"
    />
  </div>
              </CustomMarker>
            </GoogleMap>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showPopup" class="popup">
      <p>Itinerary saved successfully!</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import router from '@/router';
import { inject, watch } from 'vue';
import { GoogleMap, CustomMarker } from 'vue3-google-map';
import { getAuth } from 'firebase/auth';
import { doc, updateDoc, arrayUnion } from 'firebase/firestore';
import { db } from '@/main';
import Overlay from '@/views/overlayPage.vue'; // Ensure this is the correct path

const apiPromise = inject('apiPromise');

const userName = ref('');
const itinerary = ref(null);
const loading = ref(true);
const errorMessage = ref(null);
const isMapReady = ref(false);
const mapCenter = ref({ lat: 0, lng: 0 });
const allActivities = ref([]);
const country = ref('');
const showPopup = ref(false);
const selectedActivity = ref(null);
const getNumDays = computed(() => itinerary.value?.day_by_day_itineraries?.length || 0);

// Construct data to send
const {
  start,
  end,
  tripType,
  countryCode,
  itinerary: itineraryData,
  selectedTags,
} = router.currentRoute.value.query;
const parsedItinerary = itineraryData ? JSON.parse(itineraryData) : [];
const parsedTags = selectedTags ? JSON.parse(selectedTags) : [];

const dataToSend = {
  startDate: start || 'Missing start date',
  endDate: end || 'Missing end date',
  tripType: tripType || 'Missing trip type',
  countryCode: countryCode || 'Missing country code',
  itinerary: parsedItinerary,
  tags: parsedTags,
};

// Fetch user name
const fetchUserName = () => {
  const auth = getAuth();
  const user = auth.currentUser;
  if (user) {
    userName.value = user.displayName || 'Guest';
  }
};

// Function to save itinerary to Firestore
const saveToItinerary = async () => {
  const auth = getAuth();
  const user = auth.currentUser;

  if (user && itinerary.value) {
    const userRef = doc(db, 'users', user.uid);
    const itineraryToSave = {
  itinerary: itinerary.value,
  country: country.value,
  numDays: getNumDays.value,
  savedAt: new Date().toISOString(), // Use ISO string for consistency
};
    try {
      await updateDoc(userRef, {
        savedItineraries: arrayUnion(itineraryToSave),
      });
      showPopup.value = true;
      setTimeout(() => (showPopup.value = false), 3000);
    } catch (error) {
      console.error('Error saving itinerary:', error);
    }
  } else {
    console.warn(
      'Cannot save itinerary: missing itinerary data or user not authenticated'
    );
  }
};

// Submit data to backend and log response
const submitData = async () => {
  errorMessage.value = null;

  try {
    const response = await axios.post(
      'https://wander-backend-app-461191603321.asia-southeast1.run.app/generate-itinerary',
      dataToSend,
      {
        headers: { 'Content-Type': 'application/json' },
      }
    );
    console.log('Backend Response:', response.data);
    itinerary.value = response.data;
    allActivities.value = itinerary.value.day_by_day_itineraries.flatMap(
      (day) => day.activities
    );
    if (allActivities.value.length > 0) {
  const firstActivity = allActivities.value[0];
  if (firstActivity.location && firstActivity.location.coordinates) {
    mapCenter.value = {
      lat: firstActivity.location.coordinates.latitude,
      lng: firstActivity.location.coordinates.longitude,
    };
  }
  country.value = response.data.country || 'Unknown Country';
}
  } catch (error) {
    errorMessage.value = 'Failed to generate itinerary.';
    console.error(
      'Error during itinerary generation:',
      error.response ? error.response.data : error
    );
  } finally {
    loading.value = false;
  }
};

const focusOnActivity = (activity) => {
  if (activity.location && activity.location.coordinates) {
    mapCenter.value = {
      lat: activity.location.coordinates.latitude,
      lng: activity.location.coordinates.longitude,
    };
    selectedActivity.value = activity; // Optional: for highlighting or info windows
  } else {
    console.warn('Activity does not have valid location coordinates.');
  }
};

watch(mapCenter, (newCenter) => {
  console.log('Map center updated to:', newCenter);
  // Add any additional logic here, such as animating the map
});


onMounted(async () => {
  fetchUserName();
  await submitData();

  try {
    await apiPromise;
    isMapReady.value = true;
    console.log('Google Maps API loaded successfully');
  } catch (error) {
    console.error('Error loading Google Maps API:', error);
  }
});
</script>

<style scoped>
/* Styles from your second code block */
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,200..900;1,200..900&display=swap');
/* General styling */
.generated-itinerary {
  margin: 0;
  padding: 0;
}

.sticky-top {
  top: 0;
  position: sticky;
  z-index: 1020;
  background-color: black;
}

.user-info {
  padding: 20px;
}

.user-info h2 {
  font-size: 3rem;
}

.main-content {
  display: flex;
  height: 100vh;
}

.itinerary-summary {
  margin-bottom: 20px;
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin: 0 20px 20px 20px;
}


/* Itinerary Details */
.itinerary-details-container {
  position: relative; /* Added */
  width: 55%;
  overflow-y: auto;
  max-height: 100vh;
  padding-right: 10px;
  padding-top: 0px;
}

.itinerary-details {
  padding: 0 20px 20px 20px;
}

.itinerary-details::-webkit-scrollbar {
  width: 8px;
}

.itinerary-details::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.itinerary-details::-webkit-scrollbar-thumb {
  background-color: #888;
}

.itinerary-details::-webkit-scrollbar-thumb:hover {
  background-color: #555;
}

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

.activity-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.itinerary-item {
  background-color: #f8f9fa;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
  padding: 10px 0;
}

.place-column img {
  max-width: 150px;
  border-radius: 8px;
  margin-bottom: 3px;
}

/* Map Container */
.map-container {
  background-color: #f8f9fa;
  width: 45%;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow: hidden;
}

.map {
  width: 100%;
  height: 100%;
}

/* Save Itinerary Button */
.save-itinerary-button {
  background-color: #007bff; /* Blue background for visibility */
  border: none;
  color: white; /* White text for contrast */
  cursor: pointer;
  font-size: 16px;
  padding: 10px 20px; /* Adequate padding */
  border-radius: 5px; /* Rounded corners */
  transition: background-color 0.3s ease, color 0.3s ease;
  margin-top: 20px; /* Space above the button */
}

.save-itinerary-button:hover {
  background-color: #0056b3; /* Darker blue on hover */
  color: #ffffff;
}

/* Popup */
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

/* Close Button (if needed) */
.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 40px;
  height: 40px;
  border: 2px solid #888;
  padding-bottom: 6px;
  background-color: white;
  border-radius: 50%;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
  cursor: pointer;
  z-index: 10;
  transition: all 0.3s ease;
}

.close-button:hover {
  border-color: #666;
  color: #666;
}

.itinerary-item {
  cursor: pointer; /* Indicates clickable */
}

.itinerary-item:hover {
  background-color: #e9ecef; /* Light hover effect */
}

.marker-selected {
  border: 2px solid #007bff;
  border-radius: 50%;
}

.selected-marker-image {
  transform: scale(1.2);
  transition: transform 0.3s ease;
}

/* Media query for responsiveness */
@media (max-width: 768px) {
  .map-container {
    display: none;
  }

  .itinerary-details-container {
    width: 100%;
  }
}
</style>