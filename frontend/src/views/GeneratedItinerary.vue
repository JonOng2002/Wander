<template>
  <div class="generated-itinerary">
    <AppNavbar class="sticky-top"></AppNavbar>

    <!-- If Loading / generatedItinerary is empty -->
    <div v-if="loading" class="empty-message">Loading itinerary...</div>
    <div v-else-if="!generatedItinerary.length" class="empty-message">
      <div class="row justify-content-between align-items-center sticky-header g-0">
        <div class="col-3 date-column">
          <h2>My Itineraries</h2>
        </div>
      </div>
      <div class="no-itinerary-message">
        <p>No itinerary generated. Please <router-link to="/savedPlaces">add places</router-link> to generate an
          itinerary.</p>
      </div>
    </div>

    <!-- When Itinerary exists -->
    <div v-else class="main-content row g-0">
      <!-- Left Side: Itinerary Details -->
      <div class="col-md-6 col-12 itinerary-details">
        <div class="row justify-content-between align-items-center g-0">
          <div class="col-12 date-column">
            <h2>Your itinerary for <strong>{{ generatedItinerary[0].country }}</strong></h2>
            <p>{{ getNumDays }} days</p>
          </div>
        </div>
        <div v-for="(place, index) in generatedItinerary" :key="index" class="itinerary-row">
          <div class="time-column">{{ generateTime(index) }}</div>
          <div class="place-column">
            <h5>{{ place.name }}</h5>
            <p>{{ place.vicinity }}</p>
            <img :src="place.image" class="place-image" :alt="place.name" />
          </div>
        </div>
      </div>

      <!-- Right Side: Google Maps -->
      <div class="col-md-6 col-12 map-container">
        <div id="location-map" class="map">
          <GoogleMap :center="mapCenter" :zoom="15" style="width: 100%; height: 100%">
            <Marker v-for="place in generatedItinerary" :key="place.place_id"
              :position="{ lat: place.coordinates.latitude, lng: place.coordinates.longitude }" />
          </GoogleMap>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { getFirestore, doc, getDoc } from "firebase/firestore";
import { getAuth } from "firebase/auth";
import { GoogleMap, Marker } from 'vue3-google-map';
import { onMounted, computed } from "vue";

export default {
  name: "GeneratedItinerary",
  components: {
    GoogleMap,
    Marker,
  },
  setup() {
    const generatedItinerary = ref([]);
    const db = getFirestore();
    const loading = ref(true);
    const timeSlots = ['09:00 AM', '11:00 AM', '02:00 PM', '04:00 PM'];
    const mapCenter = ref({ lat: 35.6762, lng: 139.6503 });

    // Helper function to assign time slots to places
    const generateTime = (index) => {
      return timeSlots[index % timeSlots.length];
    };

    // Dynamically compute the number of days
    const getNumDays = computed(() => {
      return Math.ceil(generatedItinerary.value.length / 4);
    });

    // Fetch data from Firestore
    onMounted(async () => {
      loading.value = true;
      const auth = getAuth();
      const user = auth.currentUser;

      if (user) {
        const userId = user.uid;
        const userRef = doc(db, "users", userId);

        try {
          const userDoc = await getDoc(userRef);
          if (userDoc.exists()) {
            generatedItinerary.value = userDoc.data().generatedItineraries || [];

            // Update map center to the first place in the itinerary
            if (generatedItinerary.value.length > 0) {
              const firstPlace = generatedItinerary.value[0];
              mapCenter.value = { lat: firstPlace.coordinates.latitude, lng: firstPlace.coordinates.longitude };
            }
          }
        } catch (error) {
          console.error("Error getting generatedItinerary:", error);
        } finally {
          loading.value = false;
        }
      } else {
        console.error("User is not authenticated");
        loading.value = false;
      }
    });

    return {
      generatedItinerary,
      loading,
      generateTime,
      getNumDays,
      mapCenter,
    };
  },
};
</script>

<style scoped>
h2 {
  font-family: 'Cormorant Garamond', serif;
  font-weight: bolder;
}

/* For the main destination title (e.g., "Honolulu") */
.generated-itinerary h2 {
  font-family: 'Cormorant Garamond', serif;
  /* Update font style */
  font-size: 3rem;
  /* Larger font size for the destination */
  font-weight: bold;
  /* Ensure boldness */
}

.no-itinerary-message {
  text-align: center;
  font-size: 1.2rem;
  color: grey;
  margin-top: 20px;
}

/* For the subtext under the main title (e.g., 'Going solo . October . 4 days') */
.date-column p {
  font-family: 'Roboto', sans-serif;
  /* Update font style */
  font-size: 1.2rem;
  /* Adjust font size */
  color: #333;
  /* Darker color for the date information */
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
  z-index: 1020;
  /* Higher z-index to ensure navbar stays above other elements */
  background-color: black;
  /* Ensure the background remains black */
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
  display: contents;
  /* Each row with time and place */
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
  overflow: hidden;
  /* Prevent scrolling in the map */
}

.map {
  width: 100%;
  height: 100%;
}

@media (max-width: 768px) {

  /* Hide Map at Smaller Screens */
  .map-container {
    display: none;
  }
}
</style>
