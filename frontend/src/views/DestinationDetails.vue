<template>
  <div class="destination-details">
    <div class="header-row">
      <button @click="goBack" class="btn back-button">
        Back to Destinations
      </button>
      <h1 class="page-title">Top Tourist Attractions in {{ country }}</h1>
    </div>

    <div v-if="loading" class="loading">Loading...</div>

    <div v-if="!loading" class="attractions-list">
      <div v-for="attraction in attractions" :key="attraction.place_id" class="attraction-card">
        <img :src="attraction.image" alt="attraction-image" class="attraction-image" />
        <h2>{{ attraction.name }}</h2>
        <p>{{ attraction.vicinity }}</p>
        <save-place-button class="btn"
        :placeId="attraction.place_id || `manual-${Date.now()}`"  
          :placeName="attraction.name"
          :vicinity="attraction.vicinity || 'Unknown vicinity'"      
          :country="country"
          :city="cityName ||  'Unknown City'"
          :latitude="attraction.coordinates?.latitude || 0"         
          :longitude="attraction.coordinates?.longitude || 0"       
          :placePng="attraction.image || '/default-image.jpg'"     
          :userId="userId"
          :activities="[]"  
          :summary="'Google Places Summary'"
          :source="'google_places'"
        >Add to save places</save-place-button>
      </div>
    </div>

    <div v-if="showPopup" class="popup">
      <p>Added to saved places!</p>
    </div>
  </div>
</template>

<script>
import { getAuth } from "firebase/auth";
import axios from "axios";
import SavePlaceButton from "@/components/SavePlaceButton.vue";

export default {
  name: "DestinationDetails",
  components: {
    SavePlaceButton,
  },
  data() {
    return {
      attractions: [],
      loading: true,
      country: this.$route.params.country,
      apiKey: 'AIzaSyCv4guJix6s5zFZjK2GokfshsfqlLAU3Lg',
      cityName: this.$route.params.city || 'Unknown City', 
      userId: null,
      showPopup: false,
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
          place_id: place.place_id,
          name: place.name,
          vicinity: place.vicinity || this.city,
          coordinates: {
            latitude: place.geometry.location.lat,
            longitude: place.geometry.location.lng,
          },
          image: place.photos
            ? `https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${place.photos[0].photo_reference}&key=${this.apiKey}`
            : '/default-image.jpg',
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
    }
  },
  mounted() {
    const auth = getAuth();
    auth.onAuthStateChanged((user) => {
      if (user) {
        this.userId = user.uid; // Set the user ID when authenticated
      } else {
        console.error("No user is logged in");
      }
    });
  }
};
</script>

<style scoped>
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
</style>