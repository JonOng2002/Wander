import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS
import 'bootstrap/dist/js/bootstrap.bundle.js'; // Import Bootstrap JS (includes Popper.js)
import { reactive } from 'vue';

// Import BootstrapVue3 and its CSS
import BootstrapVue3 from 'bootstrap-vue-3';
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'; // Correct import for BootstrapVue3 CSS

// Define a global state for saved places
const savedPlacesState = reactive({
    savedPlaces: JSON.parse(localStorage.getItem('savedPlaces')) || [], // Load from localStorage
    addPlace(place) {
      // Check for duplicates before adding
      if (!this.savedPlaces.some(savedPlace => savedPlace.place_id === place.place_id)) {
        this.savedPlaces.push(place); // Add new place to saved places
        localStorage.setItem('savedPlaces', JSON.stringify(this.savedPlaces)); // Persist to localStorage
      }
    },
    removePlace(placeId) {
      // Optional: if you need a remove function to remove a saved place
      this.savedPlaces = this.savedPlaces.filter(place => place.place_id !== placeId);
      localStorage.setItem('savedPlaces', JSON.stringify(this.savedPlaces)); // Persist changes to localStorage
    }
});

// Define a global state for itinerary
const itineraryState = {
    itinerary: JSON.parse(localStorage.getItem('itinerary')) || [],
    addToItinerary(place) {
      this.itinerary.push(place);
      localStorage.setItem('itinerary', JSON.stringify(this.itinerary)); // Persist to localStorage
    },
    removeFromItinerary(placeId) {
      this.itinerary = this.itinerary.filter((place) => place.place_id !== placeId);
      localStorage.setItem('itinerary', JSON.stringify(this.itinerary)); // Persist to localStorage
    },
  };

const app = createApp(App);
app.provide('savedPlacesState', savedPlacesState); // Provide the global state to the app
app.provide('itineraryState', itineraryState); // Provide the global state to the app

app.use(router); // Use the router in the app
app.use(BootstrapVue3); // Use BootstrapVue3

app.mount('#app'); // Mount the Vue app
