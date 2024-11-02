<template>
  <div class="generated-itinerary">

    <!-- Show Overlay.vue when loading -->
    <Overlay v-if="loading" />

    <!-- Main Content (only displayed when loading is false) -->
    <div v-else class="content">
      <div class="main-content row g-0">
        <!-- Left Side: Itinerary Details -->
        <div class="itinerary-details-container">
          <div class="user-info">
            <button @click="goBack" class="back-button">
            <i class="fas fa-arrow-left"></i> Back
          </button>
            <h4>Review our recommendations for your trip</h4>
            <h2>Personalized itinerary for <strong>{{ userName }}</strong></h2>
            <h4>{{ country }} • {{ numDays }} days</h4>

            <button @click="deleteItinerary" class="delete-itinerary-button">
              Delete Itinerary
            </button>
          </div>

          <div class="itinerary-summary" v-if="itinerarySummary">
            <h3>Summary</h3>
            <p>{{ itinerarySummary }}</p>
          </div>

          <div class="itinerary-details">
            <div
              v-for="(day, index) in dayByDayItineraries || []"
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
                @click="focusOnActivity(activity)"
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
      <p>Itinerary deleted successfully!</p>
    </div>
    <Modal v-if="showConfirmDelete" @confirm="confirmDelete" @cancel="cancelDelete">
    <p>Are you sure you want to delete this itinerary?</p>
  </Modal>
  </div>

</template>

<script setup>
import { ref, onMounted, inject } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getAuth } from 'firebase/auth';
import { doc, updateDoc, arrayRemove, getDoc } from 'firebase/firestore';
import { db } from '@/main';
import { GoogleMap, CustomMarker } from 'vue3-google-map';
import Overlay from '@/views/overlayPage.vue';
import Modal from '@/components/ConfirmationModal.vue';

// Inject Google Maps API promise
const apiPromise = inject('apiPromise');

// Reactive properties
const userName = ref('');
const itinerary = ref(null);
const loading = ref(true);
const isMapReady = ref(false);
const mapCenter = ref({ lat: 0, lng: 0 });
const allActivities = ref([]);
const country = ref('');
const numDays = ref(0);
const showPopup = ref(false);
const selectedActivity = ref(null);
const itinerarySummary = ref('');
const dayByDayItineraries = ref([]);


// Router and route
const route = useRoute();
const router = useRouter();

// Fetch user name
const fetchUserName = () => {
  const auth = getAuth();
  const user = auth.currentUser;
  if (user) {
    userName.value = user.displayName || 'Guest';
    console.log('User Name:', userName.value);
  } else {
    console.warn('No user is currently authenticated.');
  }
};

// Function to delete itinerary
const confirmDelete = async () => {
  const auth = getAuth();
  const user = auth.currentUser;
  if (user && itinerary.value) {
    const userRef = doc(db, 'users', user.uid);
    try {
      await updateDoc(userRef, {
        savedItineraries: arrayRemove(itinerary.value),
      });
     console.log('Itinerary deleted successfully.');
      showPopup.value = true;
      setTimeout(() => (showPopup.value = false), 3000);
      router.push({ name: 'SavedItineraries' });
    } catch (error) {
      console.error('Error deleting itinerary:', error);
    }
  } else {
    console.warn('Cannot delete itinerary: missing itinerary data or user not authenticated');
  }
  
};

// Function to fetch saved itinerary from Firebase
const fetchSavedItinerary = async () => {
  const auth = getAuth();
  const user = auth.currentUser;
  if (user) {
    const userRef = doc(db, 'users', user.uid);
    try {
      const userDoc = await getDoc(userRef);
      if (userDoc.exists()) {
        const savedItineraries = userDoc.data().savedItineraries || [];
        console.log('Saved Itineraries:', savedItineraries);

        // Assuming you're passing a 'savedAt' parameter to identify the itinerary
        const savedAt = route.params.savedAt;
        console.log('Fetching itinerary with savedAt:', savedAt);
        itinerary.value = savedItineraries.find(it => it.savedAt === savedAt);

        if (itinerary.value) {
          console.log('Fetched Itinerary:', itinerary.value);

          // Assign itinerary summary
          itinerarySummary.value = itinerary.value.itinerary.itinerary_summary;
          console.log('Itinerary Summary:', itinerarySummary.value);

          // Assign day-by-day itineraries
          dayByDayItineraries.value = itinerary.value.itinerary.day_by_day_itineraries;
          console.log('Assigned day-by-day itineraries:', dayByDayItineraries.value);

          // Assign number of days
          numDays.value = itinerary.value.numDays;
          console.log('Number of Days:', numDays.value);

          // Assign country
          country.value = itinerary.value.country || 'Unknown Country';
          console.log('Country:', country.value);

          // Extract all activities for map markers
          allActivities.value = dayByDayItineraries.value.flatMap(
            day => day.activities
          );
          console.log('All Activities:', allActivities.value);

          // Set map center if activities exist
          if (allActivities.value.length > 0) {
            const firstActivity = allActivities.value[0];
            if (firstActivity.location && firstActivity.location.coordinates) {
              mapCenter.value = {
                lat: firstActivity.location.coordinates.latitude,
                lng: firstActivity.location.coordinates.longitude,
              };
              console.log('Map Center Set To:', mapCenter.value);
            }
          }
        } else {
          console.warn('Itinerary not found for savedAt:', savedAt);
        }
      } else {
        console.error('User document not found.');
      }
    } catch (error) {
      console.error('Error fetching itinerary:', error);
    } finally {
      loading.value = false;
    }
  } else {
    console.error('User not authenticated.');
    loading.value = false;
  }
};

// Function to focus on activity in map
const focusOnActivity = (activity) => {
  if (activity.location && activity.location.coordinates) {
    mapCenter.value = {
      lat: activity.location.coordinates.latitude,
      lng: activity.location.coordinates.longitude,
    };
    selectedActivity.value = activity; // Optional: for highlighting or info windows
    console.log('Focused on Activity:', activity);
  } else {
    console.warn('Activity does not have valid location coordinates.');
  }
};

const goBack = () => {
  router.push({ name: 'SavedItinerary' });
};

const showConfirmDelete = ref(false);

const deleteItinerary = () => {
  showConfirmDelete.value = true;
};

const cancelDelete = () => {
  showConfirmDelete.value = false;
};

// Fetch data on mounted
onMounted(async () => {
  fetchUserName();
  await fetchSavedItinerary();

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
/* Your existing styles */
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

/* Itinerary Details */
.itinerary-details-container {
  position: relative;
  width: 55%;
  overflow-y: auto;
  max-height: 100vh;
  padding-right: 10px;
  padding-top: 0px;
}

.itinerary-summary {
  margin-bottom: 20px;
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin: 0 20px 20px 20px;
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
  cursor: pointer; /* Indicates clickable */
}

.itinerary-item:hover {
  background-color: #e9ecef; /* Light hover effect */
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

/* Delete Itinerary Button */
.delete-itinerary-button {
  background-color: #dc3545; /* Red background for delete */
  border: none;
  color: white; /* White text for contrast */
  cursor: pointer;
  font-size: 16px;
  padding: 10px 20px; /* Adequate padding */
  border-radius: 5px; /* Rounded corners */
  transition: background-color 0.3s ease, color 0.3s ease;
  margin-top: 20px; /* Space above the button */
}

.delete-itinerary-button:hover {
  background-color: #c82333; /* Darker red on hover */
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

/* Marker Styles */
.marker-selected {
  border: 2px solid #007bff;
  border-radius: 50%;
}

.selected-marker-image {
  transform: scale(1.2);
  transition: transform 0.3s ease;
}

.back-button {
  background: none;
  border: none;
  color: #000; /* Black color */
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  margin-bottom: 10px; /* Add space below the button */
}

.back-button:hover {
  color: #333; /* Darker color on hover */
}

.back-button i {
  margin-right: 5px;
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