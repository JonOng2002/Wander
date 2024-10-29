<template>
  <div class="generated-itinerary">
    <AppNavbar class="sticky-top"></AppNavbar>

    <!-- Show GlobeLoader overlay with dynamic message if loading is true -->
    <div v-if="loading" class="loading-overlay">
      <GlobeLoader :message="currentMessage" size="5rem" />
    </div>

    <div class="content">
      <div class="user-info">
        <p>Review our recommendations for your trip</p>
        <h2 v-if="!loading">
          Personalized itinerary for <strong>{{ userName }}</strong>
        </h2>
        <div v-else class="skeleton skeleton-heading"></div>
        <p v-if="!loading">{{ country }} • {{ getNumDays }} days</p>
        <div v-else class="skeleton skeleton-text" style="width: 50%;"></div>
      </div>

      <div class="main-content row g-0">
        <!-- Left Side: Itinerary Details -->
        <div class="col-md-6 col-12 itinerary-details">
          <!-- Skeleton structure as fallback when loading is true -->
          <div v-if="loading">
            <!-- Simulating multiple days with skeleton rows -->
            <div v-for="n in 3" :key="n" class="day-section-skeleton">
              <div class="skeleton skeleton-day-header"></div>
              <div class="skeleton skeleton-day-description"></div>

              <!-- Skeleton for activities within the day -->
              <div class="itinerary-table-skeleton">
                <div class="itinerary-row-skeleton" v-for="m in 2" :key="m">
                  <div class="skeleton skeleton-time"></div>
                  <div class="skeleton skeleton-place-column">
                    <div class="skeleton skeleton-activity-name"></div>
                    <div class="skeleton skeleton-location"></div>
                    <div class="skeleton skeleton-image"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Render actual itinerary data when not loading -->
          <div v-else>
            <div v-for="(day, index) in itinerary?.day_by_day_itineraries || []" :key="index" class="day-section">
              <div class="day-header">Day {{ day.day }} : {{ day.date }}</div>
              <div class="day-description">{{ day.summary }}</div>

              <!-- Itinerary activities with skeletons for images -->
              <div class="itinerary-table">
                <div
                  class="itinerary-row"
                  v-for="(activity, actIndex) in day.activities || []"
                  :key="actIndex"
                >
                  <div class="time-column">{{ activity.time }}</div>
                  <div class="place-column">
                    <h5>{{ activity.activity_name }}</h5>
                    <p><em>Location:</em> {{ activity.location?.name || 'Unknown location' }}</p>

                    <!-- Show activity image if available; otherwise show skeleton -->
                    <div class="image-container">
                      <img
                        v-if="activity.location.photo_url"
                        :src="activity.location.photo_url"
                        class="place-image"
                        :alt="activity.activity_name"
                      />
                      <div v-else class="skeleton skeleton-image"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <button v-if="!loading && itinerary" @click="saveToItinerary" class="btn save-itinerary-button">
            Save to My Itineraries
          </button>
        </div>

        <!-- Right Side: Google Map with skeleton box as before -->
        <div class="col-md-6 col-12 map-container">
          <div v-if="isMapReady" id="location-map" class="map">
            <GoogleMap :api-promise="apiPromise" :center="mapCenter" :zoom="15" style="width: 100%; height: 100%">
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
          </div>
          <div v-else class="skeleton skeleton-map"></div>
        </div>
      </div>
    </div>

    <div v-if="showPopup" class="popup">
      <p>Itinerary saved successfully!</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onBeforeUnmount } from 'vue';
import axios from 'axios';
import router from '@/router';
import { inject } from 'vue';
import { GoogleMap, CustomMarker } from 'vue3-google-map';
import { getAuth } from 'firebase/auth';
import { doc, updateDoc, arrayUnion } from 'firebase/firestore';
import { db } from '@/main';
import GlobeLoader from '@/components/GlobeLoader.vue';

const apiPromise = inject('apiPromise');

const userName = ref('');
const itinerary = ref(null);
const loading = ref(true);
const errorMessage = ref(null);
const isMapReady = ref(false);
const mapCenter = ref({ lat: 0, lng: 0 });
const allActivities = ref([]);
const { start, end, tripType, countryCode, itinerary: itineraryData, selectedTags } = router.currentRoute.value.query;
const country = ref('');
const showPopup = ref(false);
const currentMessage = ref("Sending your details over...");
let messageIndex = 0;
let messageInterval = null;

const loadingMessages = [
  "Generating your itinerary...",
  "Fetching data from OpenAI...",
  "Fetching from PlacesAPI...",
  "Finalizing your itinerary details...",
  "Almost done! Just a moment..."
];

const startMessageRotation = () => {
  const displayDuration = 2500;
  messageInterval = setInterval(() => {
    currentMessage.value = loadingMessages[messageIndex];
    messageIndex = (messageIndex + 1) % loadingMessages.length;
  }, displayDuration);
};

const submitData = async () => {
  const parsedItinerary = itineraryData ? JSON.parse(itineraryData) : [];
  const parsedTags = selectedTags ? JSON.parse(selectedTags) : [];
  const dataToSend = { startDate: start, endDate: end, tripType, countryCode, itinerary: parsedItinerary, tags: parsedTags };

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
    }

    const activityWithCity = allActivities.value.find(activity => activity.location?.city);
    country.value = activityWithCity?.location?.city || "Unknown Location";

    const google = await apiPromise;
    if (google && google.maps) {
      isMapReady.value = true;
    }
  } catch (error) {
    errorMessage.value = 'Failed to generate itinerary.';
  } finally {
    loading.value = false;
    clearInterval(messageInterval);
  }
};

const fetchUserName = () => {
  const auth = getAuth();
  const user = auth.currentUser;
  if (user) {
    userName.value = user.displayName || "Guest";
  }
};

const getNumDays = computed(() => itinerary.value ? itinerary.value.day_by_day_itineraries.length : 0);

const saveToItinerary = async () => {
  const auth = getAuth();
  const user = auth.currentUser;
  if (user) {
    const userRef = doc(db, "users", user.uid);
    const itineraryToSave = {
      itinerary: itinerary.value,
      country: country.value,
      createdAt: new Date(),
    };
    try {
      await updateDoc(userRef, { savedItineraries: arrayUnion(itineraryToSave) });
      showPopup.value = true;
      setTimeout(() => (showPopup.value = false), 3000);
    } catch (error) {
      console.error("Error saving itinerary:", error);
    }
  }
};

onMounted(() => {
  startMessageRotation();
  fetchUserName();
  submitData();
});

onBeforeUnmount(() => {
  clearInterval(messageInterval);
});
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.85); /* Reduced opacity */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

/* Skeleton Placeholder Style */
.skeleton {
  background-color: #a9a9a9;
  border-radius: 4px;
}

/* Skeleton Heading */
.skeleton-heading {
  height: 35px;
  width: 60%;
  margin: 20px 0;
  border-radius: 8px;
}

/* Skeleton Text Line */
.skeleton-text {
  height: 18px;
  width: 50%;
  margin: 10px 0;
}

/* Skeleton for Day Section */
.skeleton-day-header {
  height: 25px;
  width: 70%;
  margin: 10px 0;
}

.skeleton-day-description {
  height: 18px;
  width: 90%;
  margin: 5px 0;
}

/* Skeleton Itinerary Table */
.itinerary-table-skeleton {
  padding: 15px;
  background-color: #f0f0f0;
  border-radius: 10px;
}

.itinerary-row-skeleton {
  display: grid;
  grid-template-columns: 1fr 3fr;
  gap: 10px;
  margin-bottom: 15px;
}

.skeleton-time {
  height: 20px;
  width: 40px;
}

.skeleton-place-column {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.skeleton-activity-name {
  height: 20px;
  width: 80%;
}

.skeleton-location {
  height: 18px;
  width: 60%;
}

.skeleton-image {
  height: 80px;
  width: 100%;
  border-radius: 8px;
}

/* Skeleton Map */
.skeleton-map {
  height: 100%;
  width: 100%;
  background-color: #a9a9a9;
  border-radius: 8px;
}

.itinerary-row {
  display: contents;
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

.sticky-top {
  top: 0;
  position: sticky;
  z-index: 1020;
  background-color: black;
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

.itinerary-details::-webkit-scrollbar {
  display: none;
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
</style>