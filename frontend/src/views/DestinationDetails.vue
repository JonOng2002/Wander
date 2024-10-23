<template>
  <div class="destination-details">
    <div class="header-row">
      <button @click="goBack" class="btn back-button">Back to Destinations</button>
      <h1 class="page-title">Top Tourist Attractions in {{ country }}</h1>
    </div>

    <div v-if="loading" class="loading">Loading...</div>

    <div v-if="!loading" class="attractions-list">
      <div v-for="attraction in attractions" :key="attraction.place_id" class="attraction-card">
        <img :src="attraction.image" alt="attraction-image" class="attraction-image" />
        <h2 class="attraction-name">{{ attraction.name }}</h2>
        <p class="attraction-vicinity">{{ attraction.vicinity }}</p>
        <save-place-button class="btn save-button" :placeId="attraction.place_id || `manual-${Date.now()}`
          " :placeName="attraction.name" :vicinity="attraction.vicinity || 'Unknown vicinity'" :country="country"
          :city="cityName || 'Unknown City'" :latitude="attraction.coordinates?.latitude || 0"
          :longitude="attraction.coordinates?.longitude || 0" :placePng="attraction.image || '/default-image.jpg'"
          :userId="userId" :activities="[]" :summary="'Google Places Summary'" :source="'google_places'"
          @place-saved="handlePlaceSaved(attraction.place_id)">
          Add to Saved Places
        </save-place-button>
      </div>
    </div>

    <div v-if="showPopup" class="popup">
      <p>Added to saved places!</p>
    </div>

    <div class="saved-places-list" v-if="savedPlaces.length > 0">
      <h2>Your Saved Places</h2>
      <ul>
        <li v-for="(place, index) in savedPlaces" :key="index">{{ place.name }} - {{ place.vicinity }}</li>
      </ul>
      <button @click="generateItinerary" class="btn generate-btn">Generate Itinerary!</button>
    </div>
  </div>
</template>

<script>
import SavePlaceButton from "@/components/SavePlaceButton.vue"; // Adjust the path as needed
import { getFirestore, doc, setDoc, runTransaction, arrayUnion } from "firebase/firestore";
import { getAuth } from "firebase/auth";
import axios from "axios";

export default {
  name: "DestinationDetails",
  components: {
    SavePlaceButton,
  },
  inject: ["savedPlacesState"],
  data() {
    return {
      attractions: [],
      loading: true,
      country: this.$route.params.country,
      apiKey: 'AIzaSyAOXjziKAewVGQL7N1IDTg1QpJNIa04TNo',
      cityName: this.$route.params.city || 'Unknown City',
      userId: null,
      showPopup: false,
      savedPlaces: [],
    };
  },
  created() {
    this.fetchAttractions();
  },
  methods: {
    handlePlaceSaved(placeId) {
      this.currentAttractionId = placeId; // Set the current attraction ID
      this.showSavedPopup(); // Show the popup

      // Save the place to the user's saved places
      this.savePlaceToFirebase(placeId);
    },
    async fetchAttractions() {
      const location = this.getCountryCoordinates(this.country);
      if (!location) {
        console.error(`No coordinates found for ${this.country}`);
        this.loading = false;
        return;
      }

      const radius = 50000;
      const type = "tourist_attraction";
      const url = `/api/maps/api/place/nearbysearch/json?location=${location}&radius=${radius}&type=${type}&key=${this.apiKey}`;

      try {
        const response = await axios.get(url);
        console.log("Fetched attractions:", response.data.results);
        this.attractions = response.data.results.map((place) => ({
          name: place.name,
          place_id: place.place_id,
          vicinity: place.vicinity,
          image: place.photos
            ? `https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${place.photos[0].photo_reference}&key=${this.apiKey}`
            : "/default-image.jpg",
        }));
        this.loading = false;
      } catch (error) {
        console.error("Error fetching attractions:", error);
        this.loading = false;
      }
    },
    getCountryCoordinates(country) {
      const coordinates = {
        'France': '48.8566,2.3522',
        'Italy': '41.9028,12.4964',
        'Japan': '35.6895,139.6917',
        'United States': '37.7749,-122.4194',
        'Spain': '40.4168,-3.7038',
        'China': '39.9042,116.4074',
        'Mexico': '19.4326,-99.1332',
        'United Kingdom': '51.5074,-0.1278',
        'Germany': '52.5200,13.4050',
        'Thailand': '13.7563,100.5018',
        'Turkey': '41.0082,28.9784',
        'Australia': '-33.8688,151.2093',
        'Brazil': '-23.5505,-46.6333',
        'Canada': '45.4215,-75.6972',
        'India': '28.6139,77.2090',
        'South Africa': '-25.7461,28.1881',
        'Russia': '55.7558,37.6176',
        'Argentina': '-34.6037,-58.3816',
        'Netherlands': '52.3676,4.9041',
        'Greece': '37.9838,23.7275',
      };
      return coordinates[country] || null;
    },
    goBack() {
      this.$router.go(-1);
    },
    showSavedPopup() {
      this.showPopup = true; // Show the popup
      setTimeout(() => {
        this.showPopup = false; // Automatically hide after 3 seconds
      }, 3000);
    },
    async savePlaceToFirebase(placeId) {
    const auth = getAuth();
    const user = auth.currentUser;

    if (user) {
        this.userId = user.uid; // Ensure this is set

        const db = getFirestore();
        const userRef = doc(db, "users", this.userId);
        const attraction = this.attractions.find(attraction => attraction.place_id === placeId);

        if (attraction) {
            const placeData = {
                place_id: attraction.place_id || null,
                name: attraction.name || 'Unknown',
                vicinity: attraction.vicinity || 'Unknown vicinity',
                image: attraction.image || '/default-image.jpg',
            };

            try {
                // Use a transaction to ensure atomic operation
                await runTransaction(db, async (transaction) => {
                    const userDoc = await transaction.get(userRef);

                    if (userDoc.exists()) {
                        const existingSavedPlaces = userDoc.data().savedPlaces || [];

                        // Check if the place already exists
                        const placeExists = existingSavedPlaces.some(savedPlace => savedPlace.place_id === placeData.place_id);

                        if (placeExists) {
                            console.log("Place already saved:", placeData.name);
                            return; // Exit if already saved
                        }
                    }

                    // If not already saved, save the new place
                    transaction.set(userRef, {
                        savedPlaces: arrayUnion(placeData),
                    }, { merge: true });
                    console.log("Place added to saved places:", placeData.name);
                    this.showSavedPopup();
                });
            } catch (error) {
                console.error("Error saving place to Firebase:", error);
            }
        } else {
            console.error("Attraction not found for saving.");
        }
    } else {
        console.error("User is not authenticated");
    }
},
  },
  mounted() {
  const auth = getAuth();
  auth.onAuthStateChanged(async (user) => {
    if (user) {
      this.userId = user.uid; // Set userId on mount
      const db = getFirestore();
      const userRef = doc(db, "users", this.userId); // Use this.userId here

      // Ensure this method is called after saving a place
      if (this.currentAttractionId) {
        const attraction = this.attractions.find(attraction => attraction.place_id === this.currentAttractionId);

        if (attraction) {
          try {
            const placeData = {
              place_id: attraction.place_id || null,
              name: attraction.name || 'Unknown',
              vicinity: attraction.vicinity || 'Unknown vicinity',
              image: attraction.image || '/default-image.jpg',
            };

            await setDoc(
              userRef,
              {
                savedPlaces: arrayUnion(placeData),
              },
              { merge: true }
            );
            console.log("Place added to saved places:", placeData.name);

            // Show the popup and hide it after 2 seconds
            this.showSavedPopup();
          } catch (error) {
            console.error("Error saving place to Firebase:", error);
          }
        } else {
          console.error("Attraction not found for saving.");
        }
      }
    } else {
      console.error("User is not authenticated");
    }
  });
}

};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap");

.destination-details {
  text-align: center;
  font-family: "Roboto", sans-serif;
}

.header-row {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px 5%;
  position: relative;
}

.back-button {
  position: absolute;
  left: 5%;
  background-color: black;
  color: white;
  border: 1px solid black;
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.back-button:hover {
  transform: scale(1.05);
  /* Keep the hover effect for scaling */
  background-color: black;
  /* Maintain the black background on hover */
  color: white;
  /* Keep the text color white on hover */
}


.page-title {
  font-size: rem;
  color: black;
  font-family: 'Cormorant Garamond', serif;
  font-weight: bolder;
}

.loading {
  font-size: 1.5rem;
  margin: 50px;
  color: black;
}

.attractions-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.attraction-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  /* Ensure space between elements to keep the button at the bottom */
  margin: 20px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 10px;
  width: 220px;
  /* Fixed width */
  height: 400px;
  /* Fixed height */
  text-align: center;
  background-color: #fff;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  /* Prevent overflow */
}

.attraction-card:hover {
  transform: translateY(-5px);
  /* Lift effect on hover */
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  /* Enhanced shadow with darker effect */
}

.attraction-image {
  width: 100%;
  height: 180px;
  /* Fixed height for the image */
  object-fit: cover;
  border-radius: 5px;
  margin-bottom: 10px;
}

h2.attraction-name {
  font-size: 1rem;
  /* Maintain font size */
  margin: 10px 0;
  color: black;
  white-space: normal;
  /* Allow text to wrap */
  overflow: visible;
  /* Ensure overflow is visible */
}

p.attraction-vicinity {
  font-size: 0.8rem;
  /* Maintain font size */
  color: gray;
  white-space: normal;
  /* Allow text to wrap */
  overflow: visible;
  /* Ensure overflow is visible */
}

.save-button {
  margin-top: auto;
  /* Push button to the bottom */
  background-color: black;
  color: white;
  padding: 8px;
  /* Reduced padding */
  font-size: 0.8rem;
  /* Maintain button font size */
  font-weight: bold;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.save-button:hover {
  background-color: #333;
  color: white;
}

/* Optional: Responsive design for smaller screens */
@media (max-width: 768px) {
  .attraction-card {
    width: 90%;
    /* Make cards wider on smaller screens */
    height: auto;
    /* Allow auto height for better fitting */
  }
}


.popup {
  position: fixed;
  bottom: 20px;
  /* Position from the bottom */
  left: 50%;
  /* Center it horizontally */
  transform: translateX(-50%);
  /* Adjust position to center */
  background-color: green;
  color: white;
  padding: 10px 20px;
  /* Add some horizontal padding */
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  /* Optional: add a shadow */
  z-index: 1000;
  /* Ensure it appears above other elements */
  transition: opacity 0.3s ease;
  /* Smooth transition for fading */
  opacity: 1;
  /* Start visible */
}
</style>
