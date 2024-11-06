<!-- src/views/ExtractedLocations.vue -->
<template>
  <div ref="extractedLocationsRoot" class="page-fade-in">
    <hr>

    <p class="header-main">Discovered from the Travel Clips!</p>
    <!-- Row of Location Images -->
    <div class="row mb-4 mx-4">
      <div
        v-for="(place, index) in allImages"
        :key="place.place_id || index"
        class="col-3"
      >
        <!-- Add cursor-pointer class to make cursor appear as a hand -->
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

    <p class="header-interested mb-5 mt-2">Interested? Scroll down for more info</p>
    <br><br>

    <p class="video-header">From your video</p>
    <p class="header-main">Main location</p>

    <!-- Horizontal Location Information Card -->
    <div
      v-if="locationInfo"
      :id="locationInfo.place_name.replace(/\s+/g, '-').toLowerCase() || 'main-location'"
      class="card mb-5 mx-auto"
      style="max-width: 1000px;"
    >
      <div class="row g-0">

        <!-- Image Section -->
        <div class="col-md-6">
          <img
            :src="locationInfo.place_png"
            @error="handleImageError"
            class="img-fluid rounded-start main-img"
            alt="Image of {{ locationInfo.place_name }}"
            style="height: 100%; object-fit: cover;"
          />
        </div>

        <!-- Content Section -->
        <div class="col-md-6">
          <div class="card-body pb-0">
            <h5 class="card-title">{{ locationInfo.place_name }}</h5>
            <p class="card-text">{{ locationInfo.location_summary }}</p>
            <div class="d-flex align-items-center">
              <StarRating :rating="locationInfo.rating" />
              <span class="card-rating ms-2">({{ locationInfo.rating.toFixed(1) }})</span>
            </div>
          </div>

          <hr>

          <!-- Location Details -->
          <div class="card-body py-0">
            <h5 class="card-title">Location</h5>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">{{ locationInfo.city }}, {{ locationInfo.country }}</li>
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
                  :center="{ lat: locationInfo.coordinates.latitude, lng: locationInfo.coordinates.longitude }"
                  :zoom="15"
                >
                  <CustomMarker
                    :key="locationInfo.place_id"
                    :options="{
                      position: {
                        lat: locationInfo.coordinates.latitude || 0,
                        lng: locationInfo.coordinates.longitude || 0,
                      },
                      anchorPoint: 'BOTTOM_CENTER',
                    }"
                  >
                    <div style="text-align: center">
                      <div style="font-size: 1.125rem">{{ locationInfo.place_name }}</div>
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

          <hr>

          <!-- Save Place Button -->
          <div class="card-body pt-0">
            <save-place-button
              class="btn btn-dark"
              :class="{ 'saved': isPlaceSaved(locationInfo.place_id) }"
              :placeId="locationInfo.place_id"
              :isAlreadySaved="isPlaceSaved(locationInfo.place_id)"
              @save-place="savePlaceToFirebase"
            >
              {{ isPlaceSaved(locationInfo.place_id) ? 'Saved' : 'Add to Saved Places' }}
            </save-place-button>
          </div>

        </div>
      </div>
    </div>

    <br>
    <br>

    <!-- Related Places Section -->
    <div v-if="relatedPlaces.length">
      <p class="related-header">Related Places</p>
      <p class="related-places-header">You might also be interested in...</p>
      <ul style="list-style-type: none; padding: 0; margin: 0;">
        <li
          v-for="place in relatedPlaces"
          :key="place.place_id"
          :id="place.place_name.replace(/\s+/g, '-').toLowerCase()"
          class="card mx-auto mb-5"
          style="max-width: 1000px;"
        >

          <div class="row g-0"> <!-- Use Bootstrap's row class for horizontal alignment -->
            <!-- Image Section -->
            <div class="col-md-6"> <!-- Adjust column size as needed -->
              <img
                :src="place.place_png"
                class="img-fluid rounded-start main-img"
                alt="Image of {{ place.place_name }}"
                @error="handleImageError"
                style="height: 100%; object-fit: cover;"
              />
            </div>

            <!-- Content Section -->
            <div class="col-md-6"> <!-- Adjust column size as needed -->
              <div class="card-body">
                <h5 class="card-title">{{ place.place_name }}</h5>
                <p class="card-text">{{ place.location_summary }}</p>
                <div class="d-flex align-items-center">
                  <StarRating :rating="place.rating" />
                  <span class="card-rating ms-2">({{ place.rating.toFixed(1) }})</span>
                </div>
                <hr>
                <h5 class="card-title">Location</h5>
                <ul class="list-group list-group-flush">
                  <li class="list-group-item">{{ place.city }}, {{ place.country }}</li>
                </ul>
                <!-- Related Places Map Section -->
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
                <hr>
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
// Helper function to generate a random alphanumeric Place ID
function generateRandomPlaceId(length = 35) {
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for(let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return result;
}

// Helper function to generate a random rating between 4.0 and 5.0 with one decimal place
function getRandomRating(min = 4.0, max = 5.0) {
  return parseFloat((Math.random() * (max - min) + min).toFixed(1));
}

import SavePlaceButton from '@/components/SavePlaceButton.vue';
import StarRating from '@/components/StarRating.vue'; // Import StarRating component
import { GoogleMap, CustomMarker } from 'vue3-google-map';
import ToastNotification from '@/components/ToastNotification.vue'; // Import the ToastNotification component
import { auth } from '@/main.js'; // Ensure auth is correctly imported

export default {
  name: "ExtractedLocations",
  inject: ['apiPromise', 'savedPlacesState'], // Inject savedPlacesState
  components: {
    SavePlaceButton,
    StarRating, // Register StarRating component
    GoogleMap,    // Register GoogleMap component
    CustomMarker, // Register CustomMarker component
    ToastNotification, // Register ToastNotification component
  },

  emits: ['component-mounted'],

  data() {
    return {
      navItems: [],
      toastShow: false, // For ToastNotification
      toastMessage: "",
      toastType: "add", // Default type for ToastNotification
      toastKey: 0, // Unique key for ToastNotification
      center: { lat: 0, lng: 0 },
      mainMapVisible: false, // New property for the main location map toggle
      navbarVisible: false, // New property to control sidebar visibility
      arrowRotated: false, // New property to track arrow rotation
      errorMessage: "", // For handling errors
      // Placeholder data for testing with randomized place IDs and ratings
      locationInfo: {
        place_id: generateRandomPlaceId(35), // Assign a longer random Place ID
        place_name: "Tokyo",
        country: "Japan",
        city: "Tokyo",
        place_png: "https://lh3.googleusercontent.com/places/ANXAkqF1CuCtTFxqFDoOfUnj-P11Bm_ifmDw1s1Nlt-hRGO4I8MbFJb_ykDmHkcLWAf9Ey-HE1efeoHpP6oZzKDOywEktfMvopE3Msk=s1600-w800",
        coordinates: {
          latitude: 35.6764225,
          longitude: 139.650027
        },
        activities: [
          "Night photography",
          "Sightseeing",
          "Cultural experiences",
          "Dining at izakayas",
          "Visiting temples"
        ],
        location_summary: "Tokyo is a vibrant metropolis known for its blend of ultramodern and traditional features, from neon-lit skyscrapers and bustling streets to historic temples and serene gardens. The city is especially captivating at night with countless photo opportunities.",
        vicinity: "Tokyo, Japan",
        rating: getRandomRating(), // Assign random rating as Number
      },
      relatedPlaces: [
        {
          place_id: generateRandomPlaceId(35), // Assign a longer random Place ID
          place_name: "Kyoto",
          country: "Japan",
          city: "Kyoto",
          place_png: "https://lh3.googleusercontent.com/places/ANXAkqFhUb_YENj1ybGqMVzejr6hQGN-s8Yp8uAwevQBmgJupIkKz1KQXwkeXTdnLEVJvIQ_OK84H8Y_N0WrOx3Lq8uwKRaZBVeVkHg=s1600-w800",
          coordinates: {
            latitude: 35.011564,
            longitude: 135.7681489
          },
          activities: [
            "Temple visits",
            "Cultural experiences",
            "Cherry blossom viewing",
            "Traditional tea ceremonies"
          ],
          location_summary: "Kyoto is famous for its classical Buddhist temples, as well as gardens, imperial palaces, Shinto shrines, and traditional wooden houses. It's a city that offers a glimpse into Japan's heritage.",
          vicinity: "Kyoto",
          mapVisible: false,
          rating: getRandomRating(), // Assign random rating as Number
        },
        {
          place_id: generateRandomPlaceId(35), // Assign a longer random Place ID
          place_name: "Osaka",
          country: "Japan",
          city: "Osaka",
          place_png: "https://lh3.googleusercontent.com/places/ANXAkqG_OA7RzCh0dKVNuw9BRSbZt8QABQn07tkCi_ufZcgrQ4KAN8xVod5p1xJ6L4L25gXZA-YtlNOh15-LkP9-hDsV7ZbkJDD9ot0=s1600-w711",
          coordinates: {
            latitude: 34.6937249,
            longitude: 135.5022535
          },
          activities: [
            "Visiting Osaka Castle",
            "Street food tasting",
            "Shopping in Namba",
            "Nightlife exploration"
          ],
          location_summary: "Osaka is known for modern architecture, nightlife, and hearty street food, and it is often considered the culinary capital of Japan, making it a great city to experience both food and fun.",
          vicinity: "Osaka",
          mapVisible: false,
          rating: getRandomRating(), // Assign random rating as Number
        },
        {
          place_id: generateRandomPlaceId(35), // Assign a longer random Place ID
          place_name: "Nara",
          country: "Japan",
          city: "Nara",
          place_png: "https://lh3.googleusercontent.com/places/ANXAkqE7CGTelnYgPqBafHNng4ywu1G4q8HoUVY9KaZV57gtuvY3mDezBDER7BCo9Yn4XWBbrZ8UK0k1bA6_izoznVg4CZn2-ctF2lE=s1600-w800",
          coordinates: {
            latitude: 34.685109,
            longitude: 135.8048019
          },
          activities: [
            "Deer park exploration",
            "Visiting Todai-ji Temple",
            "Cultural experiences"
          ],
          location_summary: "Nara is a historic city known for its temples and friendly free-roaming deer in Nara Park, making it a significant cultural site dating back to Japan's ancient capital.",
          vicinity: "Nara",
          mapVisible: false,
          rating: getRandomRating(), // Assign random rating as Number
        }
      ]
    };
  },
  computed: {
    allImages() {
      const images = [];
      if (this.locationInfo) images.push(this.locationInfo); // Add main location image
      if (this.relatedPlaces.length) images.push(...this.relatedPlaces); // Add related places images
      return images;
    },

    savedPlaceIds() {
      return this.savedPlacesState && Array.isArray(this.savedPlacesState.savedPlaces)
        ? new Set(this.savedPlacesState.savedPlaces.map(place => place.place_id))
        : new Set();
    },
  },

  methods: {
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
     * Generate navigation items based on locationInfo and relatedPlaces.
     */
    generateNavItems() {
      const items = [];

      if (this.locationInfo) {
        items.push({
          id: this.locationInfo.place_id, // Use place_id for unique identification
          name: this.locationInfo.place_name,
          active: true,
        });
      }

      this.relatedPlaces.forEach((place) => {
        items.push({
          id: place.place_id, // Use place_id for unique identification
          name: place.place_name,
          active: false,
          mapVisible: false,  // Default map visibility for related places
        });
      });

      this.navItems = items;
    },

    /**
     * Handle scroll events to update active navigation links.
     */
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

  mounted() {
    this.generateNavItems();

    if (this.locationInfo?.coordinates) {
      this.center = {
        lat: this.locationInfo.coordinates.latitude,
        lng: this.locationInfo.coordinates.longitude,
      };
    }
    this.$emit('component-mounted');

    window.addEventListener('scroll', this.handleScroll);

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
}

.header-main {
  font-weight: bold;
  text-align: center;
  font-size: x-large;
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

@media (min-width: 768px) and (max-width: 991px) {
  .card {
    width: 90%; /* Allow full-width for smaller screens */
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

/* Optional: Additional styles for SavePlaceButton */
.save-place-button {
  /* Add any additional styles if needed */
}
</style>
