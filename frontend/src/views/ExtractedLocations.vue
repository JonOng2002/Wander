<template>
  <ul class="nav flex-column contentbar">
    <li v-for="(place, index) in navItems" :key="index" class="nav-item">
      <a :class="['nav-link', place.active ? 'active' : '']" :href="`#${place.name.replace(/\s+/g, '-').toLowerCase()}`">{{ place.name }}</a>
    </li>
  </ul>

  <h3>Extracted locations</h3>

  <!-- Location Information -->
  <div v-if="locationInfo" :id="locationInfo.place_name.replace(/\s+/g, '-').toLowerCase() || 'main-location'" class="card mx-auto mb-5" style="width: 40rem;">
    <img :src="locationInfo.place_png" @error="handleImageError" class="card-img-top" alt="Image of {{ locationInfo.place_name }}">
    <div class="card-body pb-0">
      <h5 class="card-title">{{ locationInfo.place_name }}</h5>
      <p class="card-text">{{ locationInfo.summary }}</p>
    </div>
    <hr>
    <div class="card-body py-0">
      <h5 class="card-title">Location</h5>
      <ul class="list-group list-group-flush">
        <li class="list-group-item">{{ locationInfo.city }}, {{ locationInfo.country }}</li>
        <li class="list-group-item">Latitude: {{ locationInfo.coordinates.latitude }}</li>
        <li class="list-group-item">Longitude: {{ locationInfo.coordinates.longitude }}</li>
      </ul>

      <!-- Ensure Google Maps API is loaded and locationInfo is available before rendering -->
      <div v-if="apiPromiseResolved && locationInfo && locationInfo.coordinates">
        <GoogleMap :api-promise="apiPromise" style="width: 100%; height: 500px"
          :center="{ lat: locationInfo.coordinates.latitude, lng: locationInfo.coordinates.longitude }" :zoom="15">
          <Marker :options="{ position: { lat: locationInfo.coordinates.latitude, lng: locationInfo.coordinates.longitude } }" />
        </GoogleMap>
      </div>
    </div>

    <hr>
    <div class="card-body pt-0" v-if="userId">
      <save-place-button class='btn btn-dark' @place-saved="handlePlaceSaved"
        :placeName="locationInfo.place_name" :country="locationInfo.country"
        :city="locationInfo.city" :latitude="locationInfo.coordinates.latitude"
        :longitude="locationInfo.coordinates.longitude" :placePng="locationInfo.place_png" :userId="userId"
        :activities="locationInfo.activities" :summary="locationInfo.summary" :savedPlaces="savedPlaces">
      </save-place-button>
    </div>
  </div>

  <!-- Related Places Section -->
  <div v-if="relatedPlaces.length">
    <h2>Related Places</h2>
    <ul>
      <li v-for="place in relatedPlaces" :key="place.place_name" :id="place.place_name.replace(/\s+/g, '-').toLowerCase()" class="card mx-auto mb-5" style="width: 40rem;">
        <img :src="place.place_png" class="card-img-top" alt="Image of {{ place.place_name }}" @error="handleImageError">
        <div class="card-body pb-0">
          <h5 class="card-title">{{ place.place_name }}</h5>
          <p class="card-text">{{ place.summary }}</p>
        </div>
        <hr>
        <div class="card-body py-0">
          <h5 class="card-title">Location</h5>
          <ul class="list-group list-group-flush">
            <li class="list-group-item">{{ place.city }}, {{ place.country }}</li>
            <li class="list-group-item">Latitude: {{ place.coordinates.latitude }}</li>
            <li class="list-group-item">Longitude: {{ place.coordinates.longitude }}</li>
          </ul>
          <!-- Ensure Google Maps API is loaded and place coordinates are available before rendering the map -->
          <div v-if="apiPromiseResolved && place.coordinates">
            <GoogleMap :api-promise="apiPromise" style="width: 100%; height: 500px"
              :center="{ lat: place.coordinates.latitude, lng: place.coordinates.longitude }" :zoom="15">
              <Marker :options="{ position: { lat: place.coordinates.latitude, lng: place.coordinates.longitude } }" />
            </GoogleMap>
          </div>
        </div>
        <hr>
        <div class="card-body pt-0" v-if="userId">
          <save-place-button class="btn btn-dark" @place-saved="handlePlaceSaved"
            :placeName="place.place_name" :country="place.country"
            :city="place.city" :latitude="place.coordinates.latitude"
            :longitude="place.coordinates.longitude" :placePng="place.place_png" :userId="userId"
            :activities="place.activities" :summary="place.summary" :savedPlaces="savedPlaces">
          </save-place-button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import SavePlaceButton from '@/components/SavePlaceButton.vue';
import { GoogleMap, Marker } from 'vue3-google-map';
import { Loader } from '@googlemaps/js-api-loader';
import { defineProps } from 'vue';

// Props coming from parent (MainPage.vue)
const props = defineProps({
  locationInfo: Object,
  relatedPlaces: Array,
  userId: {
    type: String,
    default: '',
  },
  savedPlaces: Array,
});

// Reactive state variables
const navItems = ref([]);
const showPopup = ref(false);  // Popup visibility
const center = ref({ lat: 0, lng: 0 });

// Handle place saved popup
const handlePlaceSaved = () => {
  showPopup.value = true;
  setTimeout(() => showPopup.value = false, 2000);
};

// Load Google Maps API
const loader = new Loader({
  apiKey: 'AIzaSyDEQN9ULsxP4GwlXzrw7APt0kEssS08qbU',
  version: 'weekly',
  libraries: ['places'],
});

const apiPromise = loader.load();

const generateNavItems = () => {
  const items = [];

  // Add the main location to navItems
  if (props.locationInfo) {
    items.push({
      id: props.locationInfo.place_name,
      name: props.locationInfo.place_name,
      active: true,
    });
  }

  // Add each related place to the navItems
  props.relatedPlaces.forEach((place) => {
    items.push({
      id: place.place_name,
      name: place.place_name,
      active: false,
    });
  });

  navItems.value = items; // Assign the generated items to the navItems array
};

// Scroll handler to highlight active section
const handleScroll = () => {
  const sections = document.querySelectorAll('.card');
  const links = document.querySelectorAll('.nav-link');

  if (sections.length === 0 || links.length === 0) {
    return; // Prevent errors if elements are not found
  }

  sections.forEach((section) => {
    const rect = section.getBoundingClientRect();
    const sectionId = section.getAttribute('id');

    // Check if the section is in the viewport
    if (rect.top >= 0 && rect.top <= window.innerHeight / 2) {
      links.forEach(link => link.classList.remove('active'));
      const activeLink = document.querySelector(`.nav-link[href="#${sectionId}"]`);
      if (activeLink) activeLink.classList.add('active');
    }
  });
};

onMounted(() => {
  if (props.locationInfo?.coordinates) {
    center.value = {
      lat: props.locationInfo.coordinates.latitude,
      lng: props.locationInfo.coordinates.longitude,
    };
  }

  generateNavItems();
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});

const handleImageError = (event) => {
  event.target.src = 'https://i.postimg.cc/8zLP2XNf/Image-16-10-24-at-2-27-PM.jpg';
};
</script>

<style scoped>
html {
  scroll-behavior: smooth;
}

.contentbar {
  position: fixed;
  top: 40%;
  left: 10px;
  width: 200px;
  padding: 10px;
  border: 1px solid #ccc;
  background-color: #f8f9fa;
  border-radius: 5px;
  z-index: 1019;
}

.nav-item {
  margin-bottom: 10px;
}

.nav-link {
  color: #007bff;
  font-size: 1.1rem;
  text-decoration: none;
  transition: color 0.3s;
}

.nav-link:hover {
  color: #0056b3;
}

.nav-link.active {
  font-weight: bold;
  color: #0056b3;
  text-decoration: underline;
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
</style>