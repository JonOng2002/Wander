<template>
  <div class="generated-itinerary">
    <AppNavbar class="sticky-top" v-if="false"></AppNavbar> <!-- Navbar hidden on this page -->

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
                Embark on a captivating journey through Japan’s diverse cultural and historical gems. Your adventure
                begins with a visit to the Cup Noodles Museum Yokohama, a fascinating tribute to the history of
                instant noodles and innovation in the world of food. Immerse yourself in interactive exhibits that
                showcase the humble beginnings of this global staple, while also crafting your personalized cup
                noodles as a souvenir.
                Following this, unwind at Shichifuku No Yu, a tranquil hot spring located in Toda. This peaceful
                retreat offers an authentic Japanese bathing experience where you can relax and rejuvenate in
                mineral-rich baths amidst serene surroundings.
              </p>
              <div class="itinerary-table">
                <div class="itinerary-row" v-for="(place, timeIndex) in places" :key="timeIndex">
                  <div class="time-column">{{ generateTime(timeIndex) }}</div>
                  <div class="place-column">
                    <img :src="place.image" class="place-image" :alt="place.name" />
                    <h5>{{ place.name }}</h5>
                    <p>{{ place.vicinity }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Side: Google Maps -->
        <div class="col-md-6 map-container">
          <!-- Overlay "X" button -->
          <button class="close-button" @click="closeItinerary">×</button>
          <div id="location-map" class="map">
            <GoogleMap :center="mapCenter" :zoom="15" style="width: 100%; height: 100%">
              <Marker v-for="place in generatedItinerary" :key="place.place_id"
                :position="{ lat: place.coordinates.latitude, lng: place.coordinates.longitude }" />
            </GoogleMap>
          </div>
        </div>
      </div>

      <!-- Save to My Itineraries Button
      <button @click="saveToItinerary" class="btn save-itinerary-button">Save to My Itineraries</button>   -->
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
    // const loadGoogleMaps = async () => {
    //   const { Loader } = await import('@googlemaps/js-api-loader');
    //   const loader = new Loader({
    //     apiKey: 'AIzaSyAlRNUntEwMM5zLz3LaPQiJF68cw9uL4rE',  // Replace with your actual Google Maps API key
    //     version: 'weekly',
    //     libraries: ['places'],
    //   });

    //   loader.load().then(() => {
    //     console.log('Google Maps API loaded successfully!');
    //   }).catch((error) => {
    //     console.error('Error loading Google Maps API:', error);
    //   });
    // };

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

        console.log("Current user:", auth.currentUser);

        try {
          const userDoc = await getDoc(userRef);
          if (userDoc.exists()) {
            generatedItinerary.value = userDoc.data().generatedItineraries || [];
            console.log("Itinerary from Firebase:", generatedItinerary.value);

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

        // // Load Google Maps API
        // loadGoogleMaps();
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

    const closeItinerary = () => {
      router.push({ name: 'SavedItinerary' }); // Adjust this route if needed
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
      closeItinerary,
      navigateToSavedItinerary,
      userName,
      country,
    };
  },
};
</script>

<style scoped>
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

/* Main Content Layout */
.main-content {
  display: flex;
  height: 100vh;
  overflow: hidden;
  /* Prevent page-level scrolling */
}

/* Itinerary Container Styling */
.itinerary-details-container {
  width: 55%;
  overflow-y: auto;
  /* Only scroll the itinerary content */
  max-height: 100vh;
  padding-right: 10px;
  padding-top: 60px;
}

.itinerary-details {
  padding: 20px;
}

.itinerary-details::-webkit-scrollbar {
  width: 8px;
}

.itinerary-details::-webkit-scrollbar-track {
  background-color: #f1f1f1;
}

.itinerary-details::-webkit-scrollbar-thumb {
  background-color: #888;
}

.itinerary-details::-webkit-scrollbar-thumb:hover {
  background-color: #555;
}

/* Consistent Section Styling */
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

.itinerary-table {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  /* Two items per row */
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
  width: 45%;
  position: sticky;
  top: 0;
  height: 100vh;
  background-color: #F8F9FA;
  overflow: hidden;
}

.map {
  width: 100%;
  height: 100%;
  pointer-events: none;
}

/* Consistent Close Button Styling */
.close-button {
  position: absolute;
  top: 10px;
  right: 22px;
  width: 40px;
  height: 40px;
  border: 2px solid #888;
  background-color: white;
  padding-bottom: 6px;
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
  .map-container {
    display: none;
    /* Hide map on smaller screens */
  }

  .itinerary-details-container {
    width: 100%;
  }
}
</style>