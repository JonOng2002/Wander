<template>
  <div class="destination-details">
    <!-- Flex container to hold the back button and heading in the same row -->
    <div class="header-row">
      <!-- Back Button aligned to the left -->
      <button @click="goBack" class="btn back-button">
        Back to Destinations
      </button>

      <!-- Heading aligned to the center -->
      <h1 class="page-title">Top Tourist Attractions in {{ country }}</h1>
    </div>

    <!-- Display loading spinner while data is being fetched -->
    <div v-if="loading" class="loading">Loading...</div>

    <!-- List of destinations (attractions) -->
    <div v-if="!loading" class="attractions-list">
      <div
        v-for="attraction in attractions"
        :key="attraction.place_id"
        class="attraction-card"
      >
        <img
          :src="attraction.image"
          alt="attraction-image"
          class="attraction-image"
        />
        <h2>{{ attraction.name }}</h2>
        <p>{{ attraction.vicinity }}</p>
        <button @click="addToSavedPlaces(attraction)" class="btn">
          Add to Saved Places
        </button>
      </div>
    </div>

    <!-- Popup notification for added to saved places -->
    <div v-if="showPopup" class="popup">
      <p>Added to saved places!</p>
    </div>

    <!-- Display the saved places list -->
    <div class="saved-places-list" v-if="savedPlaces.length > 0">
      <h2>Your Saved Places</h2>
      <ul>
        <li v-for="(place, index) in savedPlaces" :key="index">
          {{ place.name }} - {{ place.vicinity }}
        </li>
      </ul>
      <button @click="generateItinerary" class="btn generate-btn">
        Generate Itinerary!
      </button>
    </div>
  </div>
</template>

<script>
import { getFirestore, doc, updateDoc, arrayUnion } from "firebase/firestore";
import { getAuth } from "firebase/auth";
import axios from "axios";


export default {
  name: "DestinationDetails",
  inject: ["savedPlacesState"],
  data() {
    return {
      attractions: [],
      loading: true,
      country: this.$route.params.country, 
      apiKey: "AIzaSyCv4guJix6s5zFZjK2GokfshsfqlLAU3Lg",
      savedPlaces: [],
      showPopup: false, // For the popup notification
    };
  },
  created() {
    this.fetchAttractions();
  },
  methods: {
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
    async addToSavedPlaces(attraction) {
      const auth = getAuth();
      const user = auth.currentUser;

      if (user) {
        const userId = user.uid;
        const db = getFirestore();
        const userRef = doc(db, "users", userId);

        try {
          await updateDoc(userRef, {
            savedPlaces: arrayUnion({
              place_id: attraction.place_id,
              name: attraction.name,
              vicinity: attraction.vicinity,
              image: attraction.image,
            }),
          });
          console.log("Place added to saved places:", attraction.name);

          // Show the popup and hide it after 2 seconds
          this.showPopup = true;
          setTimeout(() => {
            this.showPopup = false;
          }, 2000);
        } catch (error) {
          console.error("Error saving place to Firebase:", error);
        }
      } else {
        console.error("User is not authenticated");
      }
    },
    goBack() {
      this.$router.go(-1);
    },
    generateItinerary() {
      console.log("Generating itinerary with these places:", this.savedPlaces);
    },
  },
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
  background-color: lightgray;
  color: black;
  border: 1px solid black;
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: bold;
  text-transform: uppercase;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.page-title {
  font-size: 2rem;
}

.loading {
  font-size: 1.5rem;
  margin: 50px;
}

.attractions-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.attraction-card {
  margin: 20px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 10px;
  width: 200px;
  text-align: center;
  transition: transform 0.3s ease;
}

.attraction-card:hover {
  transform: scale(1.05);
}

.attraction-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 5px;
  margin-bottom: 10px;
}

h2 {
  font-size: 1.5rem;
  margin: 10px 0;
}

.btn {
  background-color: lightgray;
  color: black;
  border: 1px solid black;
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: bold;
  text-transform: uppercase;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: darkgray;
}

button {
  margin-top: 10px;
}

.saved-places-list {
  margin-top: 30px;
}

.generate-btn {
  margin-top: 20px;
}

/* Popup notification styles */
.popup {
  position: fixed;
  top: 20px;
  right: 20px;
  background-color: #4caf50;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  font-weight: bold;
  z-index: 2000;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  transition: opacity 0.3s ease;
}
</style>
