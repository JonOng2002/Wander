<template>
  <hr>
  <div class="page-fade-in">
    
    <button @click="toggleNavbar" class="btn btn-dark toggle-button arrow-toggle">
  <span class="arrow" :class="{ 'arrow-rotated': arrowRotated }"></span>

</button>

    <!-- Sidebar Navigation -->
    <div :class="['contentbar', { 'slide-in': navbarVisible, 'slide-out': !navbarVisible }]">
      <ul class="nav flex-column">
        <li v-for="(place, index) in navItems" :key="index" class="nav-item">
          <a :class="['nav-link', place.active ? 'active' : '']" :href="`#${place.name.replace(/\s+/g, '-').toLowerCase()}`">{{ place.name }}</a>
          <hr v-if="index === 0 && relatedPlaces.length > 0" class="related-divider">
        </li>
      </ul>
    </div>

  <h3 class="page-header">Extracted locations</h3>


  <!-- Location Information -->
  <div v-if="locationInfo" :id="locationInfo.place_name.replace(/\s+/g, '-').toLowerCase() || 'main-location'" class="card mx-auto mb-5" style="width: 40rem;">
    <img :src="locationInfo.place_png" @error="handleImageError" class="card-img-top" alt="Image of {{ locationInfo.place_name }}">
    <div class="card-body pb-0">
      <h5 class="card-title">{{ locationInfo.place_name }}</h5>
      <p class="card-text">{{ locationInfo.location_summary }}</p>
    </div>
    <hr>
    <div class="card-body py-0">
      <h5 class="card-title">Location</h5>
      <ul class="list-group list-group-flush">
        <li class="list-group-item">{{ locationInfo.city }}, {{ locationInfo.country }}</li>
        <li class="list-group-item"><b>Latitude:</b> {{ locationInfo.coordinates.latitude }} <b>Longitude:</b> {{ locationInfo.coordinates.longitude }}</li>
        
      </ul>
      <!-- Extracted Location Map Section -->
      <button @click="mainMapVisible = !mainMapVisible" class="btn btn-dark mb-3">
  {{ mainMapVisible ? 'Hide Map' : 'Show Map' }}
</button>

<transition name="map">
  <div v-if="mainMapVisible" id="location-map" class="map">
    <GoogleMap :api-promise="apiPromise" style="width: 100%; height: 500px"
      :center="{ lat: locationInfo.coordinates.latitude, lng: locationInfo.coordinates.longitude }" :zoom="15">
      <Marker :options="{ position: { lat: locationInfo.coordinates.latitude, lng: locationInfo.coordinates.longitude } }" />
    </GoogleMap>
  </div>
</transition>

    </div>
    
    <hr>
    <div class="card-body pt-0">
      <save-place-button class='btn btn-dark' @place-saved="handlePlaceSaved"
        :placeName="locationInfo.place_name" :country="locationInfo.country"
        :city="locationInfo.city" :latitude="locationInfo.coordinates.latitude"
        :longitude="locationInfo.coordinates.longitude" :placePng="locationInfo.place_png" :userId="userId"
        :activities="locationInfo.activities" :summary="locationInfo.location_summary" :savedPlaces="savedPlaces">
      </save-place-button>
    </div>
  </div>

  <!-- Popup for confirmation -->
  <div v-if="showPopup" class="popup">
    <p>Added to saved places!</p>
  </div>

  
  <!-- Related Places Section -->
  <div v-if="relatedPlaces.length">
    <h2 class="related-places-header">Related Places</h2>
    <ul style="list-style-type: none; /* Remove default list styling */
  padding: 0; /* Remove padding */
  margin: 0; /* Remove margin */">
      <li v-for="place in relatedPlaces" :key="place.place_name" :id="place.place_name.replace(/\s+/g, '-').toLowerCase()" class="card mx-auto mb-5" style="width: 40rem;">
        <img :src="place.place_png" class="card-img-top" alt="Image of {{ place.place_name }}" @error="handleImageError">
        <div class="card-body pb-0">
          <h5 class="card-title">{{ place.place_name }}</h5>
          <p class="card-text">{{ place.location_summary }}</p>
        </div>
        <hr>
        <div class="card-body py-0">
          <h5 class="card-title">Location</h5>
          <ul class="list-group list-group-flush">
            <li class="list-group-item">{{ place.city }}, {{ place.country }}</li>
            <li class="list-group-item"><b>Latitude:</b> {{ place.coordinates.latitude }} <b>Longitude:</b> {{ place.coordinates.longitude }}</li>
            
          </ul>
          <!-- Related Places Map Section -->
<button @click="place.mapVisible = !place.mapVisible" class="btn btn-dark mb-3">
  {{ place.mapVisible ? 'Hide Map' : 'Show Map' }}
</button>

<!-- Transition element for the sliding effect -->
<transition name="map">
  <div v-if="place.mapVisible" id="location-map" class="map">
    <GoogleMap :api-promise="apiPromise" style="width: 100%; height: 500px"
      :center="{ lat: place.coordinates.latitude, lng: place.coordinates.longitude }" :zoom="15">
      <Marker :options="{ position: { lat: place.coordinates.latitude, lng: place.coordinates.longitude } }" />
    </GoogleMap>
  </div>
</transition>


        </div>
        <hr>
        <div class="card-body pt-0">
          <save-place-button class="btn btn-dark" @place-saved="handlePlaceSaved"
            :placeName="place.place_name" :country="place.country"
            :city="place.city" :latitude="place.coordinates.latitude"
            :longitude="place.coordinates.longitude" :placePng="place.place_png" :userId="userId"
            :activities="place.activities" :summary="place.location_summary" :savedPlaces="savedPlaces">
          </save-place-button>
        </div>
      </li>
    </ul>
  </div>
  </div>
</template>

<script>
import SavePlaceButton from '@/components/SavePlaceButton.vue';
import { GoogleMap, Marker } from 'vue3-google-map';




export default {
  inject: ['apiPromise'],
  components: {
    SavePlaceButton,
    GoogleMap,    // Register GoogleMap component
    Marker        // Register Marker component
  },
  props: {
    locationInfo: Object,
    relatedPlaces: Array,
    userId: {
      type: String,
      default: '',
    },
    savedPlaces: Array,
  },

  data() {
    return {
      navItems: [],
      showPopup: false,
      center: { lat: 0, lng: 0 },
      mainMapVisible: false, // New property for the main location map toggle
      navbarVisible: false, // New property to control sidebar visibility
      arrowRotated: false, // New property to track arrow rotation
    };
  },

  methods: {
    handlePlaceSaved() {
      this.showPopup = true;
      setTimeout(() => {
        this.showPopup = false;
      }, 2000);
    },

    toggleNavbar() {
    this.navbarVisible = !this.navbarVisible;
    this.arrowRotated = !this.arrowRotated; // Toggle the rotation state on button click
  },

    generateNavItems() {
      const items = [];

      if (this.locationInfo) {
        items.push({
          id: this.locationInfo.place_name,
          name: this.locationInfo.place_name,
          active: true,
          
        });
      }

      this.relatedPlaces.forEach((place) => {
        items.push({
          id: place.place_name,
          name: place.place_name,
          active: false,
          mapVisible: false,  // Default map visibility for related places
        });
      });

      this.navItems = items;
    },

    handleScroll() {
      const sections = document.querySelectorAll('.card');
      const links = document.querySelectorAll('.nav-link');

      if (sections.length === 0 || links.length === 0) return;

      sections.forEach((section) => {
        const rect = section.getBoundingClientRect();
        const sectionId = section.getAttribute('id');

        if (rect.top >= 0 && rect.top <= window.innerHeight / 2) {
          links.forEach(link => link.classList.remove('active'));
          const activeLink = document.querySelector(`.nav-link[href="#${sectionId}"]`);
          if (activeLink) activeLink.classList.add('active');
        }
      });
    },

    handleImageError(event) {
      event.target.src = 'https://i.postimg.cc/8zLP2XNf/Image-16-10-24-at-2-27-PM.jpg';
    },
  },

  mounted() {
    this.generateNavItems();

    if (this.locationInfo?.coordinates) {
      this.center = {
        lat: this.locationInfo.coordinates.latitude,
        lng: this.locationInfo.coordinates.longitude,
      };
    }

    window.addEventListener('scroll', this.handleScroll);
  },

  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
  },
};
</script>

<style scoped>
html {
  scroll-behavior: smooth;
}

.contentbar {
  position: fixed;
  top: 40%;
  left: 65px;
  width: 200px;
  padding: 10px;
  border: 1px solid #ccc;
  background-color: white;
  border-radius: 5px;
  z-index: 1019;
  overflow-y: auto;
  transition: transform 0.3s ease; /* Smooth transition */
  transform: translateX(-100%); /* Initially hidden off-screen */
}

.contentbar.slide-in {
  transform: translateX(-33%); /* Slide in */
}

.contentbar.slide-out {
  transform: translateX(-200%); /* Slide out */
}

.arrow {
  display: inline-block;
  width: 0;
  height: 0;
  margin-right: 5px; /* Space between arrow and text */
  border-top: 5px solid transparent; /* Create the top point */
  border-bottom: 5px solid transparent; /* Create the bottom point */
  border-left: 10px solid white; /* Create the arrow color */
  transition: transform 0.3s ease; /* Transition effect for rotation */
}



.arrow-rotated {
  transform: rotate(180deg); /* Rotate the arrow */
}

.arrow-toggle {
  position: fixed;
  top: 37%; /* Position it in the middle of the screen */
  left: 0; /* Keep some space from the left edge */
  transform: translateY(-50%); /* Center it vertically */
  cursor: pointer;
  z-index: 2020; /* Ensure it's above other elements */
  transition: transform 0.3s ease; /* Smooth transition */
}



.nav-item {
  margin-bottom: 10px;
}

.nav-link {
  color: black;
  font-size: 1.1rem;
  text-decoration: none;
  
}

.nav-link:hover {
  /*text-decoration: underline;*/
  color: white;
  background-color: black;
}

.nav-link.active {
  font-weight: bold;
  color: white;
  background-color: black;

}

/* .btn {
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
} */

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




.card-img-top {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

h3,
h2 {
  text-align: center;
  font-family: "Roboto", sans-serif;
  margin: 10px 0px;
  font-size: 40px;
}

.location-map {
  height: 300px;
  width: 100%;
}

.page-header {
  font-family: 'Roboto', sans-serif;
  font-size: 3rem;
  font-weight: bold;
  text-transform: uppercase;
  color: #fff;
  background-color: black;
  padding: 20px 40px;
  text-align: center;
  letter-spacing: 0.05em;
  border-bottom: 3px solid #fff;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease-in-out;
  width: 100%;
  box-sizing: border-box; /* Ensures padding doesn't affect width */
  
}



@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.page-fade-in {
  animation: fadeIn 2s ease-in-out;
}

.related-places-header {
  font-family: 'Roboto', sans-serif;
  font-size: 1rem;
  font-weight: bold;
  text-transform: uppercase;
  color: #fff;
  background-color: black;
  padding: 20px 40px;
  text-align: center;
  letter-spacing: 0.05em;
  border-bottom: 3px solid #fff;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.3);

  margin: 0 20vw;
}

.related-divider {
  color: black;
}

/* Card Hover Effect */
.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* Smooth transition */
  border: 1px solid #ccc;
  border-radius: 10px;
  overflow: hidden;
  text-align: center;
}

/* Pop-out effect on hover */
.card:hover {
  transform: scale(1.03); /* Slightly increase the size of the card */
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2); /* Add a shadow to make it look lifted */
}

/* Ensure the card content fits within the scaled card */
.card-body {
  overflow: hidden;
}

.card {
  width: 100%; /* Take full width */
  max-width: 500px; /* Maintain a maximum width for larger screens */
  margin: 10px auto; /* Center cards */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Optional shadow for better aesthetics */
}

/* Transition styles for map */
.map-enter-active, .map-leave-active {
  transition: all 0.5s ease-in-out;
  overflow: hidden;
}

.map-enter-from, .map-leave-to {
  height: 0;
  opacity: 0;
}

.map-enter-to, .map-leave-from {
  height: 500px; /* Full height of the map */
  opacity: 1;
}



</style>