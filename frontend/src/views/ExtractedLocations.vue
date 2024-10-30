<template>
  <hr>
  <div class="page-fade-in">



    <!-- Row of Location Images -->
    <div class="row mb-4 mx-4">
      <div v-for="(place, index) in allImages" :key="index" class="col-3">
        <!-- Add cursor-pointer class to make cursor appear as a hand -->
        <div class="card h-100 position-relative cursor-pointer" @click="scrollToCard(place.place_name)">
          <img :src="place.place_png" @error="handleImageError" class="card-img-top w-100 h-100 card-href"
            :alt="`Image of ${place.place_name}`" style="object-fit: cover;">
          <div class="overlay text-center">
            <h5 class="card-title">{{ place.place_name }}</h5>
          </div>
        </div>
      </div>
    </div>


    <p class="header-interested mb-5 mt-2">Interested? Scroll down for more info</p>
    <br><br>

    <p class="video-header">From your video</p>
    <p class="header-main">Main location</p>


    <!-- Horizontal Location Information Card -->
    <div v-if="locationInfo" :id="locationInfo.place_name.replace(/\s+/g, '-').toLowerCase() || 'main-location'"
      class="card mb-5 mx-auto" style="max-width: 1000px;">
      <div class="row g-0">

        <!-- Image Section -->
        <div class="col-md-6">
          <img :src="locationInfo.place_png" @error="handleImageError" class="img-fluid rounded-start"
            alt="Image of {{ locationInfo.place_name }}" style="height: 100%; object-fit: cover;">
        </div>

        <!-- Content Section -->
        <div class="col-md-6">
          <div class="card-body pb-0">
            <h5 class="card-title">{{ locationInfo.place_name }}</h5>
            <p class="card-text">{{ locationInfo.location_summary }}</p>
          </div>

          <hr>

          

          <!-- Location Details -->
          <div class="card-body py-0">
            <h5 class="card-title">Location</h5>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">{{ locationInfo.city }}, {{ locationInfo.country }}</li>
              <li class="list-group-item"><b>Latitude:</b> {{ locationInfo.coordinates.latitude }} <b>Longitude:</b> {{
                locationInfo.coordinates.longitude }}</li>
            </ul>

            <!-- Map Toggle Button and Map -->
            <button @click="mainMapVisible = !mainMapVisible" class="btn btn-dark mb-3">
              {{ mainMapVisible ? 'Hide Map' : 'Show Map' }}
            </button>

            <transition name="map">
              <div v-if="mainMapVisible" id="location-map" class="map">
                <GoogleMap :api-promise="apiPromise" style="width: 100%; height: 500px"
                  :center="{ lat: locationInfo.coordinates.latitude, lng: locationInfo.coordinates.longitude }"
                  :zoom="15">
                  <Marker
                    :options="{ position: { lat: locationInfo.coordinates.latitude, lng: locationInfo.coordinates.longitude } }" />
                </GoogleMap>
              </div>
            </transition>
          </div>

          <hr>

          <!-- Save Place Button -->
          <div class="card-body pt-0">
            <save-place-button class='btn btn-dark' @place-saved="handlePlaceSaved" :placeName="locationInfo.place_name"
              :country="locationInfo.country" :city="locationInfo.city" :latitude="locationInfo.coordinates.latitude"
              :longitude="locationInfo.coordinates.longitude" :placePng="locationInfo.place_png" :userId="userId"
              :activities="locationInfo.activities" :summary="locationInfo.location_summary" :savedPlaces="savedPlaces">
            </save-place-button>
          </div>

        </div>
      </div>
    </div>


    <!-- Popup for confirmation -->
    <div v-if="showPopup" class="popup">
      <p>Added to saved places!</p>
    </div>

    <br>
    <br>

    <!-- Related Places Section -->
    <div v-if="relatedPlaces.length" >
      <p class="related-header">Related Places</p>
  <p class="related-places-header">You might also be interested in...</p>
  <ul style="list-style-type: none; padding: 0; margin: 0;">
    <li v-for="place in relatedPlaces" :key="place.place_name"
      :id="place.place_name.replace(/\s+/g, '-').toLowerCase()" class="card mx-auto mb-5" style="max-width: 1000px;">
      
      <div class="row g-0"> <!-- Use Bootstrap's row class for horizontal alignment -->
        <!-- Image Section -->
        <div class="col-md-6"> <!-- Adjust column size as needed -->
          <img :src="place.place_png" class="img-fluid rounded-start" alt="Image of {{ place.place_name }}"
            @error="handleImageError" style="height: 100%;  object-fit: cover;"> <!-- Ensure image fits well -->
        </div>
        
        <!-- Content Section -->
        <div class="col-md-6"> <!-- Adjust column size as needed -->
          <div class="card-body">
            <h5 class="card-title">{{ place.place_name }}</h5>
            <p class="card-text">{{ place.location_summary }}</p>
            <hr>
            <h5 class="card-title">Location</h5>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">{{ place.city }}, {{ place.country }}</li>
              <li class="list-group-item"><b>Latitude:</b> {{ place.coordinates.latitude }} <b>Longitude:</b> {{ place.coordinates.longitude }}</li>
            </ul>
            <!-- Related Places Map Section -->
            <button @click="place.mapVisible = !place.mapVisible" class="btn btn-dark mb-3">
              {{ place.mapVisible ? 'Hide Map' : 'Show Map' }}
            </button>
            <transition name="map">
              <div v-if="place.mapVisible" id="location-map" class="map">
                <GoogleMap :api-promise="apiPromise" style="width: 100%; height: 500px"
                  :center="{ lat: place.coordinates.latitude, lng: place.coordinates.longitude }" :zoom="15">
                  <Marker :options="{ position: { lat: place.coordinates.latitude, lng: place.coordinates.longitude } }" />
                </GoogleMap>
              </div>
            </transition>
            <hr>
            <save-place-button class="btn btn-dark" @place-saved="handlePlaceSaved" :placeName="place.place_name"
              :country="place.country" :city="place.city" :latitude="place.coordinates.latitude"
              :longitude="place.coordinates.longitude" :placePng="place.place_png" :userId="userId"
              :activities="place.activities" :summary="place.location_summary" :savedPlaces="savedPlaces">
            </save-place-button>
          </div>
        </div>
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
  computed: {
    allImages() {
      const images = [];
      if (this.locationInfo) images.push(this.locationInfo); // Add main location image
      if (this.relatedPlaces.length) images.push(...this.relatedPlaces); // Add related places images
      return images;
    }
  },


  methods: {
    handlePlaceSaved() {
      this.showPopup = true;
      setTimeout(() => {
        this.showPopup = false;
      }, 2000);
    },
    scrollToCard(placeName) {
      const sectionId = placeName.replace(/\s+/g, '-').toLowerCase(); // Transform the name to match the ID
      const targetSection = document.getElementById(sectionId); // Find the target section

      if (targetSection) {
        const offsetTop = targetSection.getBoundingClientRect().top + window.scrollY - 100; // Adjust -100 as needed

    window.scrollTo({
      top: offsetTop,
      behavior: 'smooth',
    });
      }
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
  transition: transform 0.3s ease;
  /* Smooth transition */
  transform: translateX(-100%);
  /* Initially hidden off-screen */
}

.contentbar.slide-in {
  transform: translateX(-33%);
  /* Slide in */
}

.contentbar.slide-out {
  transform: translateX(-200%);
  /* Slide out */
}

.arrow {
  display: inline-block;
  width: 0;
  height: 0;
  margin-right: 5px;
  /* Space between arrow and text */
  border-top: 5px solid transparent;
  /* Create the top point */
  border-bottom: 5px solid transparent;
  /* Create the bottom point */
  border-left: 10px solid white;
  /* Create the arrow color */
  transition: transform 0.3s ease;
  /* Transition effect for rotation */
}



.arrow-rotated {
  transform: rotate(180deg);
  /* Rotate the arrow */
}

.arrow-toggle {
  position: fixed;
  top: 37%;
  /* Position it in the middle of the screen */
  left: 0;
  /* Keep some space from the left edge */
  transform: translateY(-50%);
  /* Center it vertically */
  cursor: pointer;
  z-index: 2020;
  /* Ensure it's above other elements */
  transition: transform 0.3s ease;
  /* Smooth transition */
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


.location-map {
  height: 300px;
  width: 100%;
}

.header-interested {
  font-family: 'Garamond', sans-serif;

  text-align: center;

}

.header-main {
  font-family: 'Garamond', sans-serif;
  font-weight: bold;
  text-align: center;
  font-size: x-large;
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
  font-family: 'Garamond', sans-serif;
  font-weight: bold;
  text-align: center;
  font-size: x-large;

}

.related-header, .extracted-header, .video-header{
  font-family: 'Garamond', sans-serif;
  font-weight: bold;
  text-align: center;
  font-size: smaller;
  opacity: 0.5;
}



.related-divider {
  color: black;
}

/* Card Hover Effect */
.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  /* Smooth transition */
  border: 1px solid #ccc;
  border-radius: 10px;
  overflow: auto;
  text-align: center;
  background-color: #f0f6ff;
  font-family: 'Garamond', sans-serif;
}

.card-title {
  font-weight: bold;
}

/* Pop-out effect on hover */
.card:hover {
  transform: scale(1.03);
  /* Slightly increase the size of the card */
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  /* Add a shadow to make it look lifted */
}

/* Ensure the card content fits within the scaled card */
.card-body {
  overflow: hidden;

}

.card {
  width: 100%;
  /* Take full width */
  max-width: 500px;
  /* Maintain a maximum width for larger screens */
  margin: 10px auto;
  /* Center cards */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  /* Optional shadow for better aesthetics */
}

/* Transition styles for map */
.map-enter-active,
.map-leave-active {
  transition: all 0.5s ease-in-out;
  overflow: hidden;
}

.map-enter-from,
.map-leave-to {
  height: 0;
  opacity: 0;
}

.map-enter-to,
.map-leave-from {
  height: 500px;
  /* Full height of the map */
  opacity: 1;
}

li {
  background-color: #f0f6ff;
}

.overlay {
  position: absolute;
  bottom: 10px;
  /* Position the text 10px from the bottom */
  left: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  /* Align the text to the bottom */
  color: white;
  font-size: 1.25rem;
  font-weight: bold;
  text-align: center;
  padding: 5px 0;
  /* Add black outline to text */
  text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;

  border-radius: 0 0 10px 10px;
  /* Optional rounded corners */
}


.card-href {
  aspect-ratio: 1 / 1.5;
  /* Sets the aspect ratio to be 1:2 (width : height) */
  width: 100%;
  object-fit: cover;
}

.cursor-pointer {
  cursor: pointer;
  /* Changes cursor to hand on hover */
}



/* Adjust other related styles if necessary */
</style>