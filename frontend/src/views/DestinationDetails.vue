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
  import axios from "axios";
  
  export default {
    name: "DestinationDetails",
    inject: ["savedPlacesState"], // Inject the saved places state
    data() {
      return {
        attractions: [], // Array to hold the tourist attractions
        loading: true, // Loading state
        country: this.$route.params.country, // Get the country name from the route params
        apiKey: "AIzaSyCv4guJix6s5zFZjK2GokfshsfqlLAU3Lg", // Replace with your API key
        savedPlaces: [], // Array to hold the saved places
      };
    },
    created() {
      this.fetchAttractions(); // Fetch attractions when the component is created
    },
    methods: {
      // Fetch top tourist attractions for the selected country using Google Places API
      async fetchAttractions() {
        const location = this.getCountryCoordinates(this.country); // Get the coordinates of the selected country
        if (!location) {
          console.error(`No coordinates found for ${this.country}`);
          this.loading = false;
          return;
        }
  
        const radius = 50000; // 50km radius for tourist attractions
        const type = "tourist_attraction";
        const url = `/api/maps/api/place/nearbysearch/json?location=${location}&radius=${radius}&type=${type}&key=${this.apiKey}`;
  
        try {
          const response = await axios.get(url);
          this.attractions = response.data.results.map((place) => {
            return {
              name: place.name,
              place_id: place.place_id,
              vicinity: place.vicinity,
              image: place.photos
                ? `https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${place.photos[0].photo_reference}&key=${this.apiKey}`
                : "/default-image.jpg",
            };
          });
          this.loading = false;
        } catch (error) {
          console.error("Error fetching attractions:", error);
          this.loading = false;
        }
      },
      // Get the coordinates of the country
      getCountryCoordinates(country) {
        const coordinates = {
        "France": "48.8566,2.3522",
        "Italy": "41.9028,12.4964",
        "Japan": "35.6895,139.6917",
        "United States": "37.7749,-122.4194",
        "Spain": "40.4168,-3.7038",
        "China": "39.9042,116.4074",
        "Mexico": "19.4326,-99.1332",
        "United Kingdom": "51.5074,-0.1278",
        "Germany": "52.5200,13.4050",
        "Thailand": "13.7563,100.5018",
        "Turkey": "41.0082,28.9784",
        "Australia": "-33.8688,151.2093",
        "Brazil": "-23.5505,-46.6333",
        "Canada": "45.4215,-75.6972",
        "India": "28.6139,77.2090",
        "South Africa": "-25.7461,28.1881",
        "Russia": "55.7558,37.6176",
        "Argentina": "-34.6037,-58.3816",
        "Netherlands": "52.3676,4.9041",
        "Greece": "37.9838,23.7275"
  };
        return coordinates[country] || null; // Return null if no match found
      },
      // Add the selected attraction to saved places
      addToSavedPlaces(attraction) {
    const isAlreadySaved = this.savedPlacesState.savedPlaces.some(
        (place) => place.place_id === attraction.place_id
    );
    if (!isAlreadySaved) {
        this.savedPlacesState.addPlace({ ...attraction });
        console.log('Current Saved Places:', this.savedPlacesState.savedPlaces); // Log the saved places state
    } else {
        console.log(`${attraction.name} is already in saved places`);
    }
},


  
      // Method to go back to the previous page
      goBack() {
        this.$router.go(-1); // Navigates back to the previous page
      },
  
      // Generate Itinerary from saved places
      generateItinerary() {
        // Use this.savedPlaces to generate your itinerary
        console.log("Generating itinerary with these places:", this.savedPlaces);
        // Navigate to itinerary page or perform further actions
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
  
  /* Flexbox container for the back button and title */
  .header-row {
    display: flex;
    justify-content: center; /* Center the title */
    align-items: center; /* Vertically align items */
    padding: 20px 5%; /* Add padding for spacing */
    position: relative; /* Make it a positioning context for the button */
  }
  
  /* Back button positioned absolutely */
  .back-button {
    position: absolute;
    left: 5%; /* Align to the left edge */
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
  </style>
  