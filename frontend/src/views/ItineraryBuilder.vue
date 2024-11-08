<!-- frontend/src/views/ItineraryBuilder.vue -->

<template>
  <div>
    <!-- Static Image Section -->
    <div class="static-image-container">
      <div class="gradientoverlay"></div>
      <img
        src="@/assets/countries/switzerland.jpg"
        alt="Thailand"
        class="d-block w-100"
      />

      <!-- Gradient Overlay -->
      <div class="gradientoverlay"></div>

      <!-- Image Content -->
      <div class="carousel-content">
        <h1>Explore New Possibilities</h1>
        <h4>Build Your Itinerary | Shuffle Your destinations</h4>
      </div>
    </div>

    <!-- Secondary Header -->
    <div class="secondary_header">
      <div class="secondary_content">
        <h2>Manage Your Itinerary</h2>
        <h5>Organize your saved locations:</h5>
      </div>

      <div class="dropdown-container" v-motion-slide-visible-once-top>
        <div class="dropdown">
          <button @click="removeAllPlaces" class="dropdown-btn">
            Remove All
          </button>
        </div>
        <div class="dropdown">
          <button @click="generateItinerary" class="dropdown-btn">
            Generate Itinerary
          </button>
        </div>
      </div>
    </div>

    <!-- Loading and Empty States -->
    <div v-if="loading" class="empty-message">Loading itinerary...</div>
    <div v-else-if="itineraryPlaces.length === 0" class="empty-message">
      <p>No places in the itinerary.</p>
    </div>

    <!-- Itinerary Cards -->
    <div v-else class="card-grid" v-auto-animate>
      <transition-group name="list" tag="div" class="transition-wrapper">
        <div
          v-for="(place, index) in itineraryPlaces"
          :key="place.place_id"
          class="card-container"
          ref="cardRefs"
          v-motion-slide-visible-once-top
        >
          <div
            class="card destination-card"
            :style="{ backgroundImage: `url(${place.image})` }"
          >
            <div class="overlay"></div>
            <button
              @click="removePlace(place.place_id)"
              type="button"
              class="btn close-button"
              aria-label="Remove Place"
            >
              ✖
            </button>
            <div class="card-body">
              <h5 class="card-title">{{ place.name }}</h5>
              <p class="card-text">{{ place.vicinity }}, {{ place.country }}</p>

              <div class="rating-container">
                <StarRating :rating="place.rating" />
                <span class="rating-number">
                  {{ place.rating ? place.rating.toFixed(1) : 'N/A' }}
                </span>
                <span class="rating-text">/ 5</span>
              </div>

              <div class="button-container">
                <div class="rearrange-container">
                  <div class="reorder-buttons">
                    <button
                      @click="moveLeft(index)"
                      :disabled="index === 0"
                      class="move-button"
                      aria-label="Move Place Left"
                    >
                      ◀
                    </button>
                    <button
                      @click="moveRight(index)"
                      :disabled="index === itineraryPlaces.length - 1"
                      class="move-button"
                      aria-label="Move Place Right"
                    >
                      ▶
                    </button>
                  </div>

                  <!-- Question Mark Icon with Tooltip -->
                  <div class="tooltip-container">
                    <span class="question-mark" aria-label="Tooltip">
                      <font-awesome-icon :icon="['fas', 'circle-info']" class="custom-icon"/>
                      <span class="tooltip-text">
                        Use these buttons to rearrange the order of your places of interest. The sequence determines the order in which places will appear in your generated itinerary.
                      </span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition-group>
    </div>

    <!-- Toast Notification -->
    <div :class="['custom-toast', { active: toastActive }, toastType]">
      <div class="toast-content">
        <i
          :class="[
            'fas',
            toastType === 'add'
              ? 'fa-check'
              : toastType === 'remove'
              ? 'fa-info'
              : 'fa-times-circle',
            'action-icon',
          ]"
        ></i>
        <div class="message">
          <span class="text text-2">{{ toastMessage }}</span>
        </div>
        <i class="fas fa-times close" @click="closeToast" aria-label="Close Toast"></i>
        <div class="custom-progress">
          <div class="progress-bar" ref="progressBar"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from "vue"; // Removed 'watch' and added 'nextTick'
import {
  getFirestore,
  doc,
  getDoc,
  updateDoc,
} from "firebase/firestore"; // Removed 'arrayRemove' as it's not used
import { getAuth } from "firebase/auth";
import { useRouter } from "vue-router";
import { gsap } from "gsap";
import StarRating from "@/components/StarRating.vue";
import { autoAnimate } from "@formkit/auto-animate/vue"; // Ensure auto-animate is registered


export default {
  name: "ItineraryBuilder",
  components: { StarRating },
  directives: {
    autoAnimate,
  },
  setup() {
    const itineraryPlaces = ref([]); // Itinerary places from Firebase
    const loading = ref(true); // Loading state
    const db = getFirestore(); // Firestore database reference
    const auth = getAuth(); // Firebase Auth reference
    const router = useRouter(); // Vue router reference

    // Toast variables
    const toastActive = ref(false);
    const progressBar = ref(null);
    const toastMessage = ref("");
    const toastType = ref(""); // 'add', 'remove', 'error'

    let toastTimeout = null; // Keep track of the toast timeout
    let progressBarAnimation = null; // Keep track of the progress bar animation

    // Fetch itinerary places from Firebase when component mounts
    onMounted(async () => {
      const user = auth.currentUser;
      if (user) {
        try {
          const userDocRef = doc(db, "users", user.uid); // Reference to the user's document
          const userDoc = await getDoc(userDocRef); // Fetch the user document
          if (userDoc.exists()) {
            const data = userDoc.data();
            itineraryPlaces.value = data.generatedItineraries || []; // Set itinerary places
            console.log("Fetched Itinerary from Firebase:", itineraryPlaces.value);
          } else {
            console.error("User document not found.");
          }
        } catch (error) {
          console.error("Error fetching itinerary:", error);
        } finally {
          loading.value = false; // Stop loading after fetch
        }
      } else {
        console.error("User not authenticated.");
        loading.value = false; // Stop loading if no user is logged in
      }

      // Animate the cards after data is loaded
      await nextTick(); // Ensure DOM is updated before animation
      animateCards();
    });

    // Animate cards using GSAP
    const animateCards = () => {
      const cardContainers = document.querySelectorAll(".card-container");
      cardContainers.forEach((card, index) => {
        gsap.fromTo(
          card,
          { opacity: 0, y: 50 },
          { opacity: 1, y: 0, duration: 0.5, delay: index * 0.1 }
        );
      });
    };

    // Show toast notification
    const showToast = (message, type) => {
      console.log("showToast called with message:", message, "type:", type);

      // Clear any existing timeout
      if (toastTimeout) {
        clearTimeout(toastTimeout);
        toastTimeout = null;
      }

      // Kill any existing progress bar animation
      if (progressBarAnimation) {
        progressBarAnimation.kill();
        progressBarAnimation = null;
      }

      // Reset progress bar immediately
      if (progressBar.value) {
        gsap.set(progressBar.value, { scaleX: 0 });
      }

      // Set toast content and show it
      toastMessage.value = message;
      toastType.value = type; // Set the action type ('add', 'remove', 'error')
      toastActive.value = true;

      // Animate progress bar using GSAP
      if (progressBar.value) {
        progressBarAnimation = gsap.to(progressBar.value, {
          scaleX: 1,
          transformOrigin: "left",
          duration: 3,
          ease: "linear",
        });
      }

      // Set timeout to hide toast after 3 seconds
      toastTimeout = setTimeout(() => {
        toastActive.value = false;
        toastTimeout = null;

        // Kill progress bar animation when toast is hidden
        if (progressBarAnimation) {
          progressBarAnimation.kill();
          progressBarAnimation = null;
        }
      }, 3000);
    };

    // Close toast manually
    const closeToast = () => {
      if (toastTimeout) {
        clearTimeout(toastTimeout);
        toastTimeout = null;
      }
      if (progressBarAnimation) {
        progressBarAnimation.kill();
        progressBarAnimation = null;
      }
      toastActive.value = false;
    };

    // Remove a single place from the itinerary
    const removePlace = async (placeId) => {
      const placeIndex = itineraryPlaces.value.findIndex(
        (place) => place.place_id === placeId
      );
      if (placeIndex !== -1) {
        // Removed the assignment to 'removedPlace' since it's unused
        itineraryPlaces.value.splice(placeIndex, 1);
        await updateItineraryInFirestore();

        // Trigger the toast notification
        showToast("Place removed successfully!", "remove");
      }
    };

    // Remove all places with animation
    const removeAllPlaces = async () => {
      const placeCards = document.querySelectorAll(".card-container");
      // Add the GSAP animation to the place cards
      gsap.to(placeCards, {
        opacity: 0,
        scale: 0.9,
        duration: 0.5,
        stagger: 0.1,
        onComplete: async () => {
          itineraryPlaces.value = []; // Clear the itinerary locally
          await updateItineraryInFirestore();

          // Trigger the toast notification
          showToast("All places removed successfully!", "remove");
        },
      });
    };

    // Generate itinerary by navigating to another route
    const generateItinerary = () => {
      router.push({
        name: "LocationDate",
      });
    };

    // Navigate back to the previous page
    const goBack = () => {
      router.go(-1);
    };

    // Update itinerary in Firestore
    const updateItineraryInFirestore = async () => {
      const user = auth.currentUser;
      if (user) {
        const userDocRef = doc(db, "users", user.uid);
        try {
          await updateDoc(userDocRef, {
            generatedItineraries: itineraryPlaces.value,
          });
          console.log("Itinerary updated in Firestore.");
        } catch (error) {
          console.error("Error updating itinerary:", error);
          // Optionally, notify the user of the failure
          showToast("Failed to update itinerary.", "error");
        }
      }
    };

    // Move item left in the array
    const moveLeft = async (index) => {
      if (index > 0) {
        const temp = itineraryPlaces.value[index];
        itineraryPlaces.value[index] = itineraryPlaces.value[index - 1];
        itineraryPlaces.value[index - 1] = temp;
        await updateItineraryInFirestore();
        showToast("Order updated", "info");
      }
    };

    // Move item right in the array
    const moveRight = async (index) => {
      if (index < itineraryPlaces.value.length - 1) {
        const temp = itineraryPlaces.value[index];
        itineraryPlaces.value[index] = itineraryPlaces.value[index + 1];
        itineraryPlaces.value[index + 1] = temp;
        await updateItineraryInFirestore();
        showToast("Order updated.", "info");
      }
    };

    return {
      itineraryPlaces,
      loading,
      removePlace,
      removeAllPlaces,
      generateItinerary,
      goBack,
      moveLeft,
      moveRight,
      // Toast variables and functions
      toastActive,
      toastMessage,
      toastType,
      progressBar,
      showToast,
      closeToast,
    };
  },
};
</script>

<style scoped>
/* <================ HEADER IMAGE CONTAINER =================> */

.static-image-container {
  position: relative;
  height: 60vh; /* Reduced height for a more compact design */
  overflow: hidden;
}

.static-image-container img {
  height: 100%;
  width: 100%;
  object-fit: cover; /* Ensures the image covers the container */
  object-position: center; /* Centers the image */
}




.carousel-inner,
.gradientoverlay {
  height: 100%;
}

.gradientoverlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.carousel-item {
  height: 100%;
}

.carousel-item img {
  height: 100%;
  width: 100%;
  object-fit: cover;
}

.carousel-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  text-align: center;
  z-index: 2;
  width: 90%;
}

.carousel-content h1 {
  font-size: 4.5rem;
  font-weight: 700;
  margin: 0;
}

.carousel-content h4 {
  font-size: 1.5rem;
  font-weight: 500;
  margin: 0.5rem 0 0;
}

/* <=========== SECONDARY HEADER =============> */

.secondary_header {
  position: relative;
  padding: 1rem 0;
  margin-top: 2.4rem;
  margin-bottom: 4rem;
  text-align: left;
}

.secondary_content {
  padding: 0 60px;
}

.secondary_content h5 {
  color: rgb(166, 163, 163);
  margin-bottom: 1rem;
}

/* Container to align buttons side by side */
.dropdown-container {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  margin-left: 60px;
}

.dropdown-btn {
  background-color: #222;
  color: #fff;
  padding: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.dropdown-btn:hover {
  background-color: #555;
}

/* <=========== CARD GRID LAYOUT =============> */

.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  row-gap: 4rem;
  padding: 2rem;
  margin: 50px;
}

.transition-wrapper {
  display: contents;
  flex-wrap: wrap;
  justify-content: flex-start;
  gap: 15px;
  padding: 20px;
}

.card-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  overflow: hidden;
  border-radius: 1.5rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  margin: 0;
  background: rgba(0, 0, 0, 0);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-container:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px hsla(0, 0%, 0%, 0.2);
}

.destination-card {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  width: 100%;
  height: 400px;
  background-size: cover;
  background-position: center;
  border-radius: inherit;
  border: none;
  padding: 1.5rem;
  box-sizing: border-box;
  color: #ffffff;
  position: relative;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  z-index: 1;
  border-radius: inherit;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  z-index: 2;
}

.close-button:hover {
  color: red;
}

.card-body {
  padding: 1rem;
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  margin: 0;
  text-align: left;
}

.card-text {
  font-size: 0.9rem;
  color: #eaeaea;
  margin: 0.3rem 0;
  text-align: left;
}

.rating-container {
  display: flex;
  align-items: center;
  gap: 5px;
  margin: 0;
  padding: 0;
}

.rating-number {
  font-size: 1rem;
  color: #ffffff;
}

.rating-text {
  font-size: 1rem;
  color: #ffffff;
}

.button-container {
  margin-top: 0.3rem;
  width: 100%;
}

.rearrange-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.reorder-buttons {
  display: flex;
  gap: 5px;
}

.move-button {
  padding: 5px 10px;
  cursor: pointer;
  background-color: white;
  color: black;
  border: 1px solid black;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.move-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.move-button:hover:not(:disabled) {
  background-color: #3f94a7;
  color: white;
}

/* Tooltip Styles */
.tooltip-container {
  position: relative;
  display: inline-block;
}

.question-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background-color: #3f94a7;
  color: white;
  border-radius: 50%;
  font-size: 14px;
  cursor: pointer;
  border: none;
  margin-left: 0.2rem;
}

.tooltip-container .tooltip-text {
  visibility: hidden;
  width: 250px;
  background-color: #333;
  color: #fff;
  text-align: left;
  border-radius: 6px;
  padding: 10px;
  position: absolute;
  z-index: 10;
  bottom: 125%;
  left: 50%;
  transform: translateX(-10%);
  opacity: 0;
  transition: opacity 0.3s;
}

.tooltip-container .tooltip-text::after {
  content: "";
  position: absolute;
  top: 100%;
  left: 20px;
  border-width: 5px;
  border-style: solid;
  border-color: #333 transparent transparent transparent;
}

.tooltip-container:hover .tooltip-text {
  visibility: visible;
  opacity: 1;
}

/* Adjustments for smaller screens */
@media (max-width: 768px) {
  .tooltip-container .tooltip-text {
    width: 200px;
  }
}

@media (max-width: 576px) {
  .tooltip-container .tooltip-text {
    width: 180px;
  }
}

/* Toast Notification Styles */
.custom-toast {
  position: fixed;
  top: 25px;
  right: 35px;
  border-radius: 12px;
  background: #fff;
  padding: 20px 35px 20px 25px;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  border-left: 6px solid #007bff;
  overflow: hidden;
  transform: translateX(100%);
  opacity: 0;
  transition: transform 0.5s ease-in-out, opacity 0.5s ease-in-out;
  z-index: 9999;
}

.custom-toast.active {
  transform: translateX(0);
  opacity: 1;
}

.custom-toast.add {
  border-left-color: #28a745;
}

.custom-toast.add .action-icon {
  background-color: #28a745;
}

.custom-toast.remove {
  border-left-color: #17a2b8;
}

.custom-toast.remove .action-icon {
  background-color: #17a2b8;
}

.custom-toast.error {
  background: #fdecea;
  border-left-color: #dc3545;
}

.custom-toast.error .action-icon {
  background-color: #dc3545;
}

.toast-content {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding-right: 30px;
}

.action-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 35px;
  width: 35px;
  color: #fff;
  font-size: 20px;
  border-radius: 50%;
}

.message {
  display: flex;
  flex-direction: column;
  margin: 0 20px;
}

.message .text {
  font-size: 20px;
  font-weight: 600;
  font-family: "Source Sans 3", sans-serif;
  color: #666666;
}

.custom-toast .close {
  position: absolute;
  top: 10px;
  right: 15px;
  padding: 5px;
  cursor: pointer;
  opacity: 0.7;
  background: transparent;
  border: none;
  color: #666;
}

.custom-toast .close:hover {
  opacity: 1;
}

.custom-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  width: 100%;
  background: #ddd;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  width: 100%;
  background-color: #0057d9;
  transform-origin: left;
  transform: scaleX(0);
}

.custom-icon {
  font-size: 18px;
}

/* <=========== BREAKPOINTS =============> */

/* Responsive adjustments */
@media (max-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .carousel-content h1 {
    font-size: 4rem;
  }

  .carousel-content h4 {
    font-size: 1.5rem;
  }


}

@media (max-width: 992px) {
  .carousel-content h1 {
    font-size: 3rem;
  }

  .carousel-content h4 {
    font-size: 1.2rem;
  }
}

@media (max-width: 768px) {
  .dropdown-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-left: 30px;
  }

  .card-grid {
    grid-template-columns: 1fr;
  }

  .carousel-content h1 {
    font-size: 2rem;
  }

  .carousel-content h4 {
    font-size: 1rem;
  }
}

@media (max-width: 1199px) {
  .dropdown-container {
    display: flex;
    flex-direction: row;
    gap: 1rem;
    margin-left: 3.6rem;
  }
}

/* Adjustments for small screens (below 373px) */
@media (max-width: 373px) {
  /* Align the dropdown-container items in a single column */
  .dropdown-container {
    display: flex;
    flex-direction: column;
    gap: 0.5rem; /* Adjust gap as necessary for compact spacing */
    margin-left: 0; /* Remove any left margin */
    margin-right: 0; /* Remove any right margin */
    align-items: stretch; /* Make buttons take full width */
    padding: 0 50px 0 50px;
  }

  /* Make buttons full-width and uniform in size */
  .dropdown-btn {
    width: 80%; /* Ensure buttons span the full width */
    padding: 12px; /* Adjust padding for a consistent look */
    font-size: 0.9rem; /* Adjust font size for readability */
    text-align: center; /* Center-align text */
  }

  /* Adjust secondary header content */
  .secondary_content {
    padding: 0 1rem; /* Reduce padding for smaller screens */
    text-align: center; /* Center the headings */
  }

  .secondary_content h2 {
    font-size: 1.5rem; /* Adjust font size for better fit */
    margin-bottom: 0.5rem;
  }

  .secondary_content h5 {
    font-size: 0.85rem; /* Smaller font size for subtitle */
    margin-bottom: 1rem;
  }
}

</style>