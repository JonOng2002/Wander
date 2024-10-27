<template>
  <div class="generated-itinerary">
    <AppNavbar class="sticky-top"></AppNavbar>

    <!-- If Loading /generatedItinerary is empty -->
    <div v-if="loading" class="empty-message">Loading itinerary...</div>
    <div v-else-if="!generatedItinerary.length" class="empty-message">
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
    <div v-else class="main-content">
      <div class="row no-gutters">
        <!-- Left Side: Itinerary Details -->
        <div class="col-md-6 itinerary-details-container">
          <div class="itinerary-details">
            <div class="row justify-content-between align-items-center g-0">
              <div class="col-12 date-column">
                <p>Review our recommendations</p>
                <h2>Personalized itinerary for <strong>{{ userName }}</strong></h2>
                <p>{{ country }} • {{ getNumDays }} days</p>
              </div>
              <!-- Save Itinerary Button -->
              <button @click="navigateToSavedItinerary" type="button" class="save-button">Save Itinerary</button>
            </div>

            <div v-for="(places, dayIndex) in splitIntoDays(generatedItinerary)" :key="dayIndex" class="day-section">
              <div class="day-header">Day {{ dayIndex + 1 }}</div>
              <p class="day-description">
                Embark on a captivating journey through Japan’s diverse cultural and historical gems. Your adventure begins with a visit to the Cup Noodles Museum Yokohama, a fascinating tribute to the history of instant noodles and innovation in the world of food. Immerse yourself in interactive exhibits that showcase the humble beginnings of this global staple, while also crafting your personalized cup noodles as a souvenir.
                Following this, unwind at Shichifuku No Yu, a tranquil hot spring located in Toda. This peaceful retreat offers an authentic Japanese bathing experience where you can relax and rejuvenate in mineral-rich baths amidst serene surroundings.
              </p>
              <div class="itinerary-table">
                <div class="itinerary-row" v-for="(place, timeIndex) in places" :key="timeIndex">
                  <div class="time-column">{{ generateTime(timeIndex) }}</div>
                  <div class="place-column">
                    <h5>{{ place.name }}</h5>
                    <p>{{ place.vicinity }}</p>
                    <img :src="place.image" class="place-image" :alt="place.name" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Side: Google Maps -->
        <div class="col-md-6 map-container">
          <div id="location-map" class="map">
            <GoogleMap :center="mapCenter" :zoom="15" style="width: 100%; height: 100%">
              <Marker v-for="place in generatedItinerary" :key="place.place_id" :position="{ lat: place.coordinates.latitude, lng: place.coordinates.longitude }" />
            </GoogleMap>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { getFirestore, doc, getDoc, updateDoc, arrayUnion } from "firebase/firestore";
import { getAuth } from "firebase/auth";
import { setDoc } from "firebase/firestore";
import { GoogleMap, Marker } from 'vue3-google-map';
import { onMounted, computed } from "vue"; // Ensure computed is imported
import router from "@/router";

export default {
  name: "GeneratedItinerary",
  components: {
    GoogleMap,
    Marker,
  },
  setup() {
    const generatedItinerary = ref([]);
    const db = getFirestore();
    const userName = ref(""); // Define userName as a ref
    const country = ref("");  // Define country as a ref
    const loading = ref(true);
    const timeSlots = ['09:00 AM', '11:00 AM', '02:00 PM', '04:00 PM'];
    const mapCenter = ref({ lat: 35.6762, lng: 139.6503 });  // Default center for Tokyo, Japan

    // Google Maps API initialization (directly in the component)
    const loadGoogleMaps = async () => {
      const { Loader } = await import('@googlemaps/js-api-loader');
      const loader = new Loader({
        apiKey: 'AIzaSyAlRNUntEwMM5zLz3LaPQiJF68cw9uL4rE',  // Replace with your actual Google Maps API key
        version: 'weekly',
        libraries: ['places'],
      });

      loader.load().then(() => {
        console.log('Google Maps API loaded successfully!');
      }).catch((error) => {
        console.error('Error loading Google Maps API:', error);
      });
    };

    // Helper function to assign time slots to places
    const generateTime = (index) => {
      return timeSlots[index % timeSlots.length];
    };

    // Mock function to split itinerary into days, say each day has 4 places
    const splitIntoDays = (itinerary) => {
      const days = [];
      const daySize = 4;  // Number of places per day
      for (let i = 0; i < itinerary.length; i += daySize) {
        days.push(itinerary.slice(i, i + daySize));
      }
      return days;
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
            generatedItinerary.value = userDoc.data().generatedItinerary || [];

            // If there are places, update the map center to the first place in the itinerary
            if (generatedItinerary.value.length > 0) {
              const firstPlace = generatedItinerary.value[0];
              country.value = firstPlace.country || "Unknown Location";  // Ensure that you have a country field in your data
              mapCenter.value = { lat: firstPlace.coordinates.latitude, lng: firstPlace.coordinates.longitude };
            }

            // Fetch userName
            userName.value = user.displayName || "Guest";
          } else {
            await setDoc(userRef, { generatedItinerary: [] });
          }
        } catch (error) {
          console.error("Error getting generatedItinerary:", error);
        } finally {
          loading.value = false;
        }

        // Load Google Maps API
        loadGoogleMaps();
      } else {
        console.error("User is not authenticated");
        loading.value = false;
      }
    });

    // Function to save the itinerary to the Firestore database
    const saveItinerary = async () => {
      const auth = getAuth();
      const user = auth.currentUser;
      if (user) {
        const userId = user.uid;
        const itineraryToSave = {
          itinerary: generatedItinerary.value,  // Ensure this contains image URLs
          country: country.value,               // Country name
          numDays: getNumDays.value,            // Number of days
          savedAt: new Date().toISOString(),    // Timestamp for itinerary was saved
          userName: user.displayName || "Guest"            // Include the user's name here as well
        };

        try {
          await updateDoc(doc(db, "users", userId), {
            savedItineraries: arrayUnion(itineraryToSave) // Add the itinerary to saved itineraries
          });
          console.log("Itinerary saved to savedItineraries successfully");
          console.log(generatedItinerary.value); // Check if all places have the 'image' field

        } catch (error) {
          console.error("Error saving itinerary:", error);
        }
      } else {
        console.error("User is not authenticated");
      }
    };


  const navigateToSavedItinerary = () => {
    saveItinerary();
    router.push({ name: "SavedItinerary" });
  }

    return {
      generatedItinerary,
      loading,
      splitIntoDays,
      generateTime,
      getNumDays,
      mapCenter,
      navigateToSavedItinerary,
      userName,
      country,
    };
  },
};
</script>

<style scoped>
/* Main Content Layout */
.main-content {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  height: 100vh;
  overflow: hidden; /* Prevent the content from overflowing */
}

/* Itinerary Container Styling */
.itinerary-details-container {
  display: flex;
  flex-direction: column;
  overflow-y: auto; /* Make only the itinerary section scrollable */
  width: 50%;
  max-height: 100vh; /* Keep the height fixed */
  padding-right: 0; /* Ensure no padding interferes with scrollbar */
}

.itinerary-details {
  padding: 20px;
}

.itinerary-details::-webkit-scrollbar {
  width: 10px; /* Scrollbar width */
}

.itinerary-details::-webkit-scrollbar-track {
  background-color: #f1f1f1; /* Scrollbar track color */
}

.itinerary-details::-webkit-scrollbar-thumb {
  background-color: #888; /* Scrollbar color */
}

.itinerary-details::-webkit-scrollbar-thumb:hover {
  background-color: #555; /* Scrollbar color on hover */
}

/* Save Itinerary Button */
.save-button {
  background-color: #333;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  border-radius: 5px;
  display: inline-block;
  margin-top: 20px;
  float: right;
}

.save-button:hover {
  background-color: #555;
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
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.5rem;
  margin-top: 10px;
  margin-bottom: 10px;
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

/* Map Container */
.map-container {
  background-color: #F8F9FA;
  height: 100vh;
  width: 50%;
  position: fixed;
  right: 0;
  top: 0;
  overflow: hidden; /* Prevent map scrolling */
}

.map {
  width: 100%;
  height: 100%;
  pointer-events: none; /* Disable map interactions */
}

/* Media query for responsiveness */
@media (max-width: 768px) {
  .map-container {
    display: none; /* Hide map below sm breakpoint */
  }

  .itinerary-details-container {
    width: 100%; /* Make itinerary take full width */
  }
}
</style>