<template>
  <div ref="extractedLocationsRoot" class="page-fade-in">
    <hr />

    <p class="header-main">Discovered From Your Travel Clips!</p>
    
    <!-- Row of Location Images -->
    <div class="row mb-4 mx-4">
      <div
        v-for="(place, index) in allImages"
        :key="place.place_id || index"
        class="col-3"
      >
        <!-- Clickable Card -->
        <div
          class="card h-100 position-relative cursor-pointer"
          @click="scrollToCard(place.place_name)"
        >
          <img
            :src="place.place_png"
            @error="handleImageError"
            class="card-img-top w-100 h-100 card-href"
            :alt="`Image of ${place.place_name}`"
            style="object-fit: cover;"
          />
          <div class="overlay text-center">
            <h5 class="card-title">{{ place.place_name }}</h5>
          </div>
        </div>
      </div>
    </div>

    <p class="header-interested mb-5 mt-2">Interested? Click the images for more info</p>
    <br /><br />

    <p class="video-header">From your video</p>
    <p class="header-main">Main location</p>

    <!-- Main Location Information Card -->
    <div
      v-if="processedLocationInfo"
      :id="processedLocationInfo.place_name.replace(/\s+/g, '-').toLowerCase() || 'main-location'"
      class="card mb-5 mx-auto"
      style="max-width: 1000px;"
    >
      <div class="row g-0">
        <!-- Image Section -->
        <div class="col-md-6">
          <img
            :src="processedLocationInfo.place_png"
            @error="handleImageError"
            class="img-fluid rounded-start main-img"
            :alt="`Image of ${processedLocationInfo.place_name}`"
            style="height: 100%; object-fit: cover;"
          />
        </div>

        <!-- Content Section -->
        <div class="col-md-6">
          <div class="card-body pb-0">
            <h5 class="card-title">{{ processedLocationInfo.place_name }}</h5>
            <p class="card-text">{{ processedLocationInfo.location_summary }}</p>
            <div class="d-flex align-items-center justify-content-center">
              <span>Rating: </span>&nbsp;
              <StarRating :rating="processedLocationInfo.rating" />
              <span class="card-rating ms-2">({{ processedLocationInfo.rating.toFixed(1) }})</span>
            </div>
          </div>

          <hr>



          <!-- Location Details -->
          <div class="card-body py-0">
            <h5 class="card-title">Location</h5>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">{{ processedLocationInfo.city }}, {{ processedLocationInfo.country }}</li>
            </ul>

            <!-- Map Toggle Button and Map -->
            <button @click="toggleMainMap" class="btn btn-dark mb-3">
              {{ mainMapVisible ? 'Hide Map' : 'Show Map' }}
            </button>

            <transition name="map">
              <div v-if="mainMapVisible" id="location-map" class="map">
                <GoogleMap
                  :api-promise="apiPromise"
                  style="width: 100%; height: 500px"
                  :center="{ lat: processedLocationInfo.coordinates.latitude, lng: processedLocationInfo.coordinates.longitude }"
                  :zoom="15"
                >
                  <CustomMarker
                    :key="processedLocationInfo.place_id"
                    :options="{
                      position: {
                        lat: processedLocationInfo.coordinates.latitude || 0,
                        lng: processedLocationInfo.coordinates.longitude || 0,
                      },
                      anchorPoint: 'BOTTOM_CENTER',
                    }"
                  >
                    <div style="text-align: center">
                      <div style="font-size: 1.125rem">{{ processedLocationInfo.place_name }}</div>
                      <img
                        src="https://i.postimg.cc/8zLP2XNf/Image-16-10-24-at-2-27-PM.jpg"
                        width="1px"
                        height="1px"
                        style="margin-top: 8px"
                      />
                    </div>
                  </CustomMarker>
                </GoogleMap>
              </div>
            </transition>
          </div>

          <hr />

          <!-- Save Place Button -->
          <div class="card-body pt-0">
            <save-place-button
              class="btn btn-dark"
              :class="{ 'saved': isPlaceSaved(processedLocationInfo.place_id) }"
              :placeId="processedLocationInfo.place_id"
              :isAlreadySaved="isPlaceSaved(processedLocationInfo.place_id)"
              @save-place="savePlaceToFirebase"
            >
              {{ isPlaceSaved(processedLocationInfo.place_id) ? 'Saved' : 'Add to Saved Places' }}
            </save-place-button>
          </div>
        </div>
      </div>
    </div>

    <br /><br />

    <!-- Related Places Section -->
    <div v-if="processedRelatedPlaces.length">
      <p class="related-header">Related Places</p>
      <p class="related-places-header">You might also be interested in...</p>
      <ul style="list-style-type: none; padding: 0; margin: 0;">
        <li
          v-for="place in processedRelatedPlaces"
          :key="place.place_id"
          :id="place.place_name.replace(/\s+/g, '-').toLowerCase()"
          class="card mx-auto mb-5"
          style="max-width: 1000px;"
        >
          <div class="row g-0">
            <!-- Image Section -->
            <div class="col-md-6">
              <img
                :src="place.place_png"
                class="img-fluid rounded-start main-img"
                :alt="`Image of ${place.place_name}`"
                @error="handleImageError"
                style="height: 100%; object-fit: cover;"
              />
            </div>

            <!-- Content Section -->
            <div class="col-md-6">
              <div class="card-body">
                <h5 class="card-title">{{ place.place_name }}</h5>
                <p class="card-text">{{ place.location_summary }}</p>
                <div class="d-flex align-items-center justify-content-center">
                  <span>Rating: </span>&nbsp;
                  <StarRating :rating="place.rating" />
                  <span class="card-rating ms-2">({{ place.rating.toFixed(1) }})</span>
                </div>
                <hr />
                <h5 class="card-title">Location</h5>
                <ul class="list-group list-group-flush">
                  <li class="list-group-item">{{ place.city }}, {{ place.country }}</li>
                </ul>
                
                <!-- Related Place Map Toggle and Map -->
                <button @click="togglePlaceMap(place)" class="btn btn-dark mb-3">
                  {{ place.mapVisible ? 'Hide Map' : 'Show Map' }}
                </button>
                
                <transition name="map">
                  <div v-if="place.mapVisible" id="location-map" class="map">
                    <GoogleMap
                      :api-promise="apiPromise"
                      style="width: 100%; height: 500px"
                      :center="{ lat: place.coordinates.latitude, lng: place.coordinates.longitude }"
                      :zoom="15"
                    >
                      <CustomMarker
                        :key="place.place_id"
                        :options="{
                          position: {
                            lat: place.coordinates.latitude || 0,
                            lng: place.coordinates.longitude || 0,
                          },
                          anchorPoint: 'BOTTOM_CENTER',
                        }"
                      >
                        <div style="text-align: center">
                          <div style="font-size: 1.125rem">{{ place.place_name }}</div>
                          <img
                            src="https://i.postimg.cc/8zLP2XNf/Image-16-10-24-at-2-27-PM.jpg"
                            width="10"
                            height="10"
                            style="margin-top: 8px"
                          />
                        </div>
                      </CustomMarker>
                    </GoogleMap>
                  </div>
                </transition>
                <hr />
                
                <!-- Save Place Button -->
                <save-place-button
                  class="btn btn-dark"
                  :class="{ 'saved': isPlaceSaved(place.place_id) }"
                  :placeId="place.place_id"
                  :isAlreadySaved="isPlaceSaved(place.place_id)"
                  @save-place="savePlaceToFirebase"
                >
                  {{ isPlaceSaved(place.place_id) ? 'Saved' : 'Add to Saved Places' }}
                </save-place-button>
              </div>
            </div>
          </div>
        </li>
      </ul>
    </div>

    <!-- Toast Notification -->
    <ToastNotification
      :key="toastKey"
      :show="toastShow"
      :message="toastMessage"
      :type="toastType"
      :duration="3000"
      @update:show="toastShow = $event"
    />
  </div>
</template>

<script>
// Helper function to generate deterministic place_id based on place properties
function generateDeterministicPlaceId(place) {
  // Concatenate unique properties to form a unique string
  const uniqueString = `${place.place_name}-${place.city}-${place.country}-${place.coordinates.latitude}-${place.coordinates.longitude}`;
  
  // Replace spaces and special characters with hyphens and convert to lowercase
  return uniqueString
    .replace(/\s+/g, '-')       // Replace spaces with hyphens
    .replace(/[^a-zA-Z0-9-]/g, '') // Remove all characters except letters, numbers, and hyphens
    .toLowerCase();             // Convert to lowercase
}

function getDeterministicRating(placeId, min = 4.0, max = 5.0) {
  let hash = 0;
  for (let i = 0; i < placeId.length; i++) {
    hash = placeId.charCodeAt(i) + ((hash << 5) - hash);
    hash = hash & hash; // Convert to 32bit integer
  }
  const normalized = (Math.abs(hash) % 1000) / 1000; // Normalize to 0 - 0.999
  return parseFloat((min + normalized * (max - min)).toFixed(1)); // Scale to min - max
}

import SavePlaceButton from '@/components/SavePlaceButton.vue';
import StarRating from '@/components/StarRating.vue'; // Import StarRating component
import { GoogleMap, CustomMarker } from 'vue3-google-map';
import ToastNotification from '@/components/ToastNotification.vue'; // Import the ToastNotification component
import { auth } from '@/main.js'; // Ensure auth is correctly imported

export default {
  name: "ExtractedLocations",
  
  // Inject dependencies
  inject: ['apiPromise', 'savedPlacesState'], // Inject savedPlacesState
  
  // Register components
  components: {
    SavePlaceButton,
    StarRating, // Register StarRating component
    GoogleMap,    // Register GoogleMap component
    CustomMarker, // Register CustomMarker component
    ToastNotification, // Register ToastNotification component
  },

  // Define props received from the backend
  props: {
    locationInfo: {
      type: Object,
      required: true,
    },
    relatedPlaces: {
      type: Array,
      required: true,
    },
  },

  // Define data properties
  data() {
    return {
      navItems: [],
      toastShow: false, // For ToastNotification
      toastMessage: "",
      toastType: "add", // Default type for ToastNotification
      toastKey: 0, // Unique key for ToastNotification
      center: { lat: 0, lng: 0 },
      mainMapVisible: false, // Toggle main location map
      navbarVisible: false, // Control sidebar visibility
      arrowRotated: false, // Track arrow rotation
      errorMessage: "", // For handling errors
      // Processed data with place_id and rating
      processedLocationInfo: null,
      processedRelatedPlaces: [],
    };
  },

  // Define computed properties
  computed: {
    // Aggregate all images for rendering
    allImages() {
      const images = [];
      if (this.processedLocationInfo) images.push(this.processedLocationInfo); // Add main location image
      if (this.processedRelatedPlaces.length) images.push(...this.processedRelatedPlaces); // Add related places images
      return images;
    },

    // Create a Set of saved place IDs for quick lookup
    savedPlaceIds() {
      return this.savedPlacesState && Array.isArray(this.savedPlacesState.savedPlaces)
        ? new Set(this.savedPlacesState.savedPlaces.map(place => place.place_id))
        : new Set();
    },
  },

  watch: {
    locationInfo: {
      handler(newVal) {
        this.initializeData(newVal, this.relatedPlaces);
      },
      deep: true,
      immediate: true, // Ensures the handler is called immediately with the initial value
    },
    relatedPlaces: {
      handler(newVal) {
        this.initializeData(this.locationInfo, newVal);
      },
      deep: true,
      immediate: true,
    },
  },

  // Define methods
  methods: {
    /**
     * Initialize processedLocationInfo and processedRelatedPlaces with place_id and rating
     * Should be called once, typically in mounted()
     * @param {Object} locationInfo - The main location data from backend
     * @param {Array} relatedPlaces - The related places data from backend
     */
    initializeData(locationInfo, relatedPlaces) {
      if (!locationInfo) return;

      // Assign deterministic place_id and rating to locationInfo if not already present
      if (!locationInfo.place_id) {
        const newPlaceId = generateDeterministicPlaceId(locationInfo);
        this.processedLocationInfo = {
          ...locationInfo,
          place_id: newPlaceId,
          rating: getDeterministicRating(newPlaceId),
        };
      } else {
        this.processedLocationInfo = { 
          ...locationInfo,
          rating: getDeterministicRating(locationInfo.place_id) || locationInfo.rating,
        };
      }

      // Process relatedPlaces with deterministic place_id and rating
      if (Array.isArray(relatedPlaces)) {
        this.processedRelatedPlaces = relatedPlaces.map(place => {
          // Assign deterministic place_id and rating if not present
          if (!place.place_id) {
            const newPlaceId = generateDeterministicPlaceId(place);
            return {
              ...place,
              place_id: newPlaceId,
              rating: getDeterministicRating(newPlaceId),
              mapVisible: false, // Initialize mapVisible property
            };
          } else {
            return {
              ...place,
              rating: getDeterministicRating(place.place_id) || place.rating,
              mapVisible: false,
            };
          }
        });
      }
    },

    /**
     * Show a toast notification for a successfully saved place.
     */
    showSavedToast() {
      this.resetToast();
      this.$nextTick(() => {
        this.toastMessage = "Added to Saved Places!";
        this.toastType = "add"; // Use 'add' type for positive feedback
        this.toastKey += 1; // Update the key to force re-render
        setTimeout(() => {
          this.toastShow = true; // Show the toast
        }, 100); // Short delay to allow DOM update
      });
    },

    /**
     * Show a toast notification for an already saved place.
     */
    displayAlreadySavedToast() {
      this.resetToast();
      this.$nextTick(() => {
        this.toastMessage = "Place has already been saved!";
        this.toastType = "info"; // Use 'info' type for informational feedback
        this.toastKey += 1; // Update the key to force re-render
        setTimeout(() => {
          this.toastShow = true; // Show the toast
        }, 100);
      });
    },

    /**
     * Show an error toast notification.
     * @param {String} message - The error message to display.
     */
    showErrorToast(message) {
      this.resetToast();
      this.$nextTick(() => {
        this.toastMessage = message;
        this.toastType = "error"; // Use 'error' type for failure
        this.toastKey += 1; // Update the key to force re-render
        setTimeout(() => {
          this.toastShow = true; // Show the toast
        }, 100);
      });
    },

    /**
     * Reset the toast state to hide any existing toast.
     */
    resetToast() {
      this.toastShow = false;
    },

    /**
     * Scroll to the specific card section based on place name.
     * @param {String} placeName - The name of the place to scroll to.
     */
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

    /**
     * Toggle the visibility of the navbar.
     */
    toggleNavbar() {
      this.navbarVisible = !this.navbarVisible;
      this.arrowRotated = !this.arrowRotated; // Toggle the rotation state on button click
    },

    /**
     * Toggle the visibility of the main location map.
     */
    toggleMainMap() {
      this.mainMapVisible = !this.mainMapVisible;
    },

    /**
     * Toggle the visibility of a related place's map.
     * @param {Object} place - The related place object.
     */
    togglePlaceMap(place) {
      place.mapVisible = !place.mapVisible;
    },

    /**
     * Handle image loading errors by setting a default image.
     * @param {Event} event - The error event.
     */
    handleImageError(event) {
      event.target.src = 'https://i.postimg.cc/8zLP2XNf/Image-16-10-24-at-2-27-PM.jpg';
    },

    /**
     * Checks if a place is already saved.
     * @param {String} placeId - The unique identifier of the place.
     * @returns {Boolean} - True if the place is saved, else false.
     */
    isPlaceSaved(placeId) {
      if (
        this.savedPlacesState &&
        Array.isArray(this.savedPlacesState.savedPlaces)
      ) {
        return this.savedPlaceIds.has(placeId);
      }
      return false;
    },

    /**
     * Saves a place to Firebase and updates the global savedPlacesState.
     * @param {String} placeId - The unique identifier of the place to save.
     */
    async savePlaceToFirebase(placeId) {
      const user = auth.currentUser;

      if (user) {
        const userId = user.uid;

        // Find the place data based on placeId
        const attraction = this.allImages.find(
          (place) => place.place_id === placeId
        );

        if (attraction) {
          const placeData = {
            place_id: attraction.place_id || null,
            name: attraction.place_name || "Unknown",
            vicinity: attraction.vicinity || "Unknown vicinity",
            image: attraction.place_png || "https://i.postimg.cc/8zLP2XNf/Image-16-10-24-at-2-27-PM.jpg",
            coordinates: {
              latitude: attraction.coordinates.latitude || 0,
              longitude: attraction.coordinates.longitude || 0,
            },
            rating: typeof attraction.rating === 'number' ? attraction.rating : parseFloat(attraction.rating) || 4.5, // Ensure rating is a number
            user_ratings_total: attraction.user_ratings_total || 0,
            city: attraction.city || "Unknown City",
            country: attraction.country || "Unknown Country",
            source: "travel_clips",
            summary: attraction.location_summary || "No summary available.",
            activities: attraction.activities || [],
          };

          try {
            // Use the global state to add the place
            const wasAdded = await this.savedPlacesState.addPlace(userId, placeData);
            console.log(`Was the place added? ${wasAdded}`);
            if (wasAdded) {
              this.showSavedToast();
            } else {
              this.displayAlreadySavedToast();
            }
          } catch (error) {
            console.error("Error saving place to Firebase:", error);
            this.showErrorToast("Failed to save the place. Please try again.");
          }
        } else {
          console.error("Place data not found for saving.");
          this.showErrorToast("Place data is missing. Unable to save.");
        }
      } else {
        console.error("User is not authenticated");
        this.showErrorToast("You must be logged in to save places.");
      }
    },
  },

  // Lifecycle hooks
  mounted() {
    this.$emit('component-mounted');

    // Initialize data without watchers
    this.initializeData(this.locationInfo, this.relatedPlaces);
    // Removed generateNavItems() call as it's undefined
    // this.generateNavItems();

    if (this.processedLocationInfo?.coordinates) {
      this.center = {
        lat: this.processedLocationInfo.coordinates.latitude,
        lng: this.processedLocationInfo.coordinates.longitude,
      };
    }

    // Listen for authentication state changes
    auth.onAuthStateChanged((user) => {
      if (user) {
        const userId = user.uid;
        // Load saved places for the authenticated user
        if (
          this.savedPlacesState &&
          typeof this.savedPlacesState.loadSavedPlaces === "function"
        ) {
          this.savedPlacesState.loadSavedPlaces(userId);
        }
      } else {
        console.error("User is not authenticated");
        // Clear the global savedPlacesState
        if (
          this.savedPlacesState &&
          typeof this.savedPlacesState.clearSavedPlaces === "function"
        ) {
          this.savedPlacesState.clearSavedPlaces();
        }
      }
    });

    // Handle scroll if handleScroll is defined
    // If handleScroll is not defined, remove these lines or define the method
    // window.addEventListener('scroll', this.handleScroll);
  },
  

  beforeUnmount() {
    // Remove scroll listener if handleScroll is defined
    // If handleScroll is not defined, remove this line
    // window.removeEventListener('scroll', this.handleScroll);
  },
};
</script>


<style scoped>
html {
  scroll-behavior: smooth;
}

/* Toast Notification Styles (handled by the ToastNotification component) */

/* Image Styles */
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
  font-weight: bold;
  text-align: center;
  font-size: 1rem;
}

.header-main {
  font-weight: bold;
  text-align: center;
  font-size: 2rem;
}

.video-header {
  font-weight: bold;
  text-align: center;
  font-size: smaller;
  opacity: 0.5;
}

.related-header,
.extracted-header,
.related-places-header {
  font-weight: bold;
  text-align: center;
  font-size: x-large;
}

.related-places-header {
  font-size: large;
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

/* List Styles */
li {
  background-color: #f0f6ff;
}

/* Overlay Styles */
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

.card-text {
  font-weight: normal;
  font-size: large;
}

.card-rating {
  font-weight: bold;
  color: #ff9800; /* Orange color for ratings */
}

@media (max-width: 1199px) {
  .card {
    width: 90%;
    /* Allow full-width for smaller screens */
  }
}

/* Adjust other related styles if necessary */
.main-img {
  aspect-ratio: 16 / 9; /* Set the desired ratio, e.g., 16:9 */
  width: 100%;
  height: auto;
  object-fit: cover;
}

/* Style for saved places */
.saved {
  background-color: #4caf50; /* Green background to indicate saved */
  color: white;
}

.btn-dark.saved:hover {
  background-color: #45a049; /* Darker green on hover */
}



/* Loading Indicator Styles (Optional) */
.loading {
  text-align: center;
  font-size: 1.5rem;
  padding: 50px;
  color: #555;
}
</style>
