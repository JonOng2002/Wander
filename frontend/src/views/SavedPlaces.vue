<!-- C:\wamp64\www\WAD2_Project\WadProj\frontend\src\views\SavedPlaces.vue -->

<template>
  <div
    id="carouselExampleInterval"
    class="carousel slide"
    data-bs-ride="carousel"
  >
    <div class="carousel-inner">
      <div class="carousel-item active" data-bs-interval="10000">
        <img
          src="@/assets/countries/thailand.jpg"
          alt="Image 1"
          class="d-block w-100"
        />
      </div>
      <div class="carousel-item" data-bs-interval="2000">
        <img
          src="@/assets/countries/denmark.jpg"
          alt="Image 2"
          class="d-block w-100"
        />
      </div>
      <div class="carousel-item">
        <img
          src="@/assets/countries/germany.jpg"
          alt="Image 3"
          class="d-block w-100"
        />
      </div>
    </div>

    <div class="itinerary-page">
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
          <i class="fas fa-times close" @click="closeToast"></i>
          <div class="custom-progress">
            <div class="progress-bar" ref="progressBar"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Gradient Overlay -->
    <div class="gradientoverlay"></div>

    <button
      class="carousel-control-prev"
      type="button"
      data-bs-target="#carouselExampleInterval"
      data-bs-slide="prev"
    >
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>
    <button
      class="carousel-control-next"
      type="button"
      data-bs-target="#carouselExampleInterval"
      data-bs-slide="next"
    >
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>

    <div class="carousel-content">
      <h1>Archive Your Journey</h1>
      <h4>Detail Your Trips | Make Lasting Memories</h4>
    </div>
  </div>

  <div class="secondary_header">
    <div class="secondary_content">
      <h2>Access your saved locations</h2>
      <h5>Locations saved, at your fingertips:</h5>
    </div>

    <div class="dropdown-container" v-motion-slide-visible-once-top>
      <div class="dropdown">
        <select @change="filterPlaces" class="dropdown-btn form-select me-2">
          <option value="">
            Select Filter
          </option>
          <option value="alphabetical">Filter by Alphabet</option>
          <option value="recently-added">Filter by Recently Added</option>
        </select>
      </div>

      <div class="dropdown">
        <button @click="deleteAllPlaces" class="dropdown-btn">
          Delete All
        </button>
      </div>

      <div class="dropdown">
        <button @click="toggleModal" class="dropdown-btn">
          View Itinerary
        </button>
      </div>

      <div class="dropdown">
        <button @click="navigateToGeneratedItinerary" class="dropdown-btn">
          View Full Itinerary
        </button>
      </div>
    </div>
  </div>

  <div v-if="loading" class="empty-message">Loading saved places...</div>
  <div
    v-else-if="filteredPlaces && filteredPlaces.length === 0"
    class="empty-message"
  >
    <p>No places saved yet. Start exploring now!</p>
  </div>

  <div v-else class="card-grid">
    <transition-group name="list" tag="div" class="transition-wrapper">
      <div
        v-for="place in filteredPlaces"
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
            @click="removePlace(place)"
            type="button"
            class="btn close-button"
          >
            ✖
          </button>
          <div class="card-body">
            <h5 class="card-title">{{ place.name }}</h5>
            <p class="card-text">{{ place.vicinity }}, {{ place.country }}</p>

            <div class="rating-container">
              <StarRating :rating="place.rating" />
              <!-- Your StarRating component -->
              <span class="rating-number">
                {{ place.rating ? place.rating.toFixed(1) : 'N/A' }}
              </span>
              <span class="rating-text">/ 5</span>
              <!-- Add text like "/ 5" if desired -->
            </div>

            <div class="button-container">
              <button
                @click="toggleItinerary(place, $event)"
                type="button"
                class="btn itinerary-button"
              >
                {{
                  isPlaceInItinerary(place)
                    ? "Remove from Itinerary"
                    : "Add to Itinerary"
                }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition-group>
  </div>

  <div v-if="showModal" class="modal-overlay" @click.self="toggleModal">
    <div class="modal-content">
      <h3>Your Itinerary</h3>
      <ol class="list-group list-group-numbered">
        <li
          class="list-group-item"
          v-for="(item, index) in itinerary"
          :key="index"
        >
          <img
            :src="item.image"
            class="modal-image"
            alt="Image of {{ item.name }}"
          />
          {{ item.name }} - {{ item.vicinity }}
        </li>
      </ol>
      <button
        @click="navigateToGeneratedItinerary"
        class="btn mb-2 view-full-itinerary-btn"
      >
        View Full Itinerary
      </button>
      <button @click="toggleModal" type="button" class="btn close-modal-btn">
        Close
      </button>
    </div>
  </div>

  <div
    v-if="showDeletePopup"
    class="modal-overlay"
    @click.self="toggleDeletePopup"
  >
    <div class="modal-content">
      <h3>Are you sure you want to delete all saved places?</h3>
      <button @click="confirmDeleteAllPlaces" type="button" class="btn mb-2">
        Yes, Delete All
      </button>
      <button
        @click="toggleDeletePopup"
        type="button"
        class="btn close-modal-btn"
      >
        Cancel
      </button>
    </div>
  </div>

  <div class="popup-container">
    <div v-if="showPopup" class="popup">
      <p>Added to itinerary!</p>
    </div>
    <div v-if="showRemovePopup" class="popup" style="background-color: #f44336">
      <p>Removed from itinerary!</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import {
  getFirestore,
  doc,
  getDoc,
  setDoc,
  updateDoc,
  arrayUnion,
  arrayRemove,
} from "firebase/firestore";
import { getAuth } from "firebase/auth";
import { useRouter } from "vue-router";
import { gsap } from "gsap";
import StarRating from "@/components/StarRating.vue";

export default {
  name: "SavedPlaces",
  components: { StarRating },

  setup() {
    const savedPlaces = ref([]);
    const filteredPlaces = ref([]);
    const itinerary = ref([]);
    const loading = ref(true);
    const showModal = ref(false);
    const showDeletePopup = ref(false);
    const db = getFirestore();
    const router = useRouter();
    const cardRefs = ref([]);

    // Reactive variables for toast notification
    const toastActive = ref(false);
    const progressBar = ref(null);
    const toastTitle = ref("");
    const toastMessage = ref("");
    const toastType = ref(""); // Type of toast notification (add or remove)

    let toastTimeout = null; // Keep track of the toast timeout
    let progressBarAnimation = null; // Keep track of the progress bar animation

    // Fetching data from Firestore and storing it in savedPlaces
    onMounted(async () => {
      const auth = getAuth();
      const user = auth.currentUser;
      await loadUserItinerary(); // Ensure itineraries are loaded first

      if (user) {
        const userId = user.uid;
        const userRef = doc(db, "users", userId);

        try {
          const userDoc = await getDoc(userRef);
          if (userDoc.exists()) {
            savedPlaces.value = userDoc.data().savedPlaces || [];
            filteredPlaces.value = [...savedPlaces.value];
          } else {
            await setDoc(userRef, { savedPlaces: [] });
            savedPlaces.value = [];
            filteredPlaces.value = [];
          }
        } catch (error) {
          console.error("Error fetching saved places:", error);
        } finally {
          loading.value = false;
        }
      } else {
        console.error("User is not authenticated");
        loading.value = false;
      }
    });

    cardRefs.value.forEach((card, index) => {
    // Perform animations or operations on each card
    gsap.fromTo(card, { opacity: 0 }, { opacity: 1, duration: 1, delay: index * 0.1 });
  });

    // Show toast notification
    const showToast = (title, message, type) => {
      console.log("showToast called with title:", title, "message:", message);

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
      toastTitle.value = title;
      toastMessage.value = message;
      toastType.value = type; // Set the action type ('add' or 'remove')
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

    const navigateToGeneratedItinerary = () => {
      router.push({
        name: "ItineraryBuilder",
      });
    };

    const isPlaceInItinerary = (place) => {
      return itinerary.value.some((item) => item.place_id === place.place_id);
    };

    const deleteAllPlaces = async () => {
      toggleDeletePopup(); // Show delete confirmation popup
    };

    const togglePopup = (type) => {
      if (type === "add") {
        showToast("Success", "Added to Itinerary!", "add");
      } else if (type === "remove") {
        showToast("Success", "Removed from Itinerary!", "remove");
      } else if (type === "error") {
        showToast("Error", "An error occurred.", "error");
      }
    };

    const toggleDeletePopup = () => {
      showDeletePopup.value = !showDeletePopup.value; // Toggle delete confirmation popup
    };

    const loadUserItinerary = async () => {
      const user = getAuth().currentUser;

      if (user) {
        const userId = user.uid;
        const userDocRef = doc(db, "users", userId);

        try {
          const docSnap = await getDoc(userDocRef);
          if (docSnap.exists()) {
            itinerary.value = docSnap.data().generatedItineraries || [];
            // Update the state for each place based on loaded itinerary
          } else {
            console.error("No such document!");
          }
        } catch (error) {
          console.error("Error fetching user itinerary:", error);
        }
      }
    };

    const toggleItinerary = async (place, event) => {
      const isInItinerary = isPlaceInItinerary(place); // Check if the place is in the itinerary

      const user = getAuth().currentUser;

      if (!user) {
        console.error("User is not authenticated");
        return;
      }

      const userId = user.uid;
      const userDocRef = doc(db, "users", userId);

      try {
        if (isInItinerary) {
          // Find the exact object in itinerary
          const itemToRemove = itinerary.value.find(
            (item) => item.place_id === place.place_id
          );

          if (!itemToRemove) {
            console.error("Item to remove not found in itinerary.");
            return;
          }

          // Remove from itinerary locally first
          itinerary.value = itinerary.value.filter(
            (item) => item.place_id !== place.place_id
          );
          togglePopup("remove"); // Show remove toast

          // Update Firebase after local state change
          try {
            await updateDoc(userDocRef, {
              generatedItineraries: arrayRemove(itemToRemove),
            });

            console.log("Place removed from itinerary:", itemToRemove);
          } catch (error) {
            console.error("Error removing itinerary from Firebase:", error);
            // Optionally, revert the local state change if Firebase update fails
            itinerary.value.push(itemToRemove);
            showToast("Error", "Failed to remove place from itinerary.", "error");
          }
        } else {
          // Construct placeData matching Firestore structure
          const placeData = {
            place_id: place.place_id || null,
            name: place.name || "Unknown",
            vicinity: place.vicinity || "Unknown vicinity",
            image: place.image || "/default-image.jpg",
            coordinates: place.coordinates || { latitude: null, longitude: null },
            rating: place.rating || 0,
            user_ratings_total: place.user_ratings_total || 0,
            open_now: place.open_now || false,
            city: place.city || "Unknown City",
            country: place.country || "Unknown Country",
            source: "google_places",
            summary: "Google Places Summary",
            activities: [],
          };

          // GSAP animation for button
          const button = event.currentTarget;

          gsap.fromTo(
            button,
            { scale: 1 },
            {
              scale: 1.1,
              duration: 0.2,
              yoyo: true,
              repeat: 1,
            }
          );

          // Add to itinerary locally first
          itinerary.value.push(placeData);
          togglePopup("add"); // Show add toast

          // Update Firebase after local state change
          try {
            await updateDoc(userDocRef, {
              generatedItineraries: arrayUnion(placeData),
            });

            console.log("Place added to itinerary:", placeData);
          } catch (error) {
            console.error("Error adding itinerary to Firebase:", error);
            // Optionally, revert the local state change if Firebase update fails
            itinerary.value = itinerary.value.filter(
              (item) => item.place_id !== place.place_id
            );
            showToast("Error", "Failed to add place to itinerary.", "error");
          }
        }
      } catch (error) {
        console.error("Error updating itinerary in Firebase:", error);
      }
    };

    // Ensure modal remains open if the place is still in generatedItineraries
    const toggleModal = async () => {
      showModal.value = !showModal.value;

      if (showModal.value) {
        try {
          const user = getAuth().currentUser;
          if (user) {
            const userId = user.uid;
            const userDocRef = doc(db, "users", userId);

            const userDoc = await getDoc(userDocRef);
            if (userDoc.exists()) {
              const data = userDoc.data().generatedItineraries;
              itinerary.value = data || [];
            } else {
              console.log("No document found for the user.");
            }
          } else {
            console.error("User is not authenticated.");
          }
        } catch (error) {
          console.error(
            "Error fetching generatedItineraries from Firebase:",
            error
          );
        }
      }
    };

    const removePlace = (place) => {
      const index = savedPlaces.value.findIndex(
        (item) => item.place_id === place.place_id
      );
      if (index !== -1) {
        savedPlaces.value.splice(index, 1);
        filteredPlaces.value = [...savedPlaces.value];

        const auth = getAuth();
        const user = auth.currentUser;

        if (user) {
          const userId = user.uid;
          const userRef = doc(db, "users", userId);

          setDoc(userRef, { savedPlaces: savedPlaces.value }, { merge: true })
            .then(() => {
              console.log("Firestore updated successfully.");
              showToast("Success", "Place Removed!", "remove");
            })
            .catch((error) => {
              console.error("Error updating Firestore:", error);
              showToast("Error", "Failed to remove place.", "error");
            });
        }
      } else {
        console.log("Place not found in saved places.");
      }
    };

    const filterPlaces = (event) => {
      const value = event.target.value;
      if (value === "alphabetical") {
        filterAlphabetically();
      } else if (value === "recently-added") {
        filterRecentlyAdded();
      } else {
        filteredPlaces.value = [...savedPlaces.value];
      }
    };

    const filterAlphabetically = () => {
      filteredPlaces.value = [...savedPlaces.value].sort((a, b) =>
        a.name.localeCompare(b.name)
      );
    };

    const filterRecentlyAdded = () => {
      // Ensure that each place has a 'dateAdded' field. If not, this will not sort correctly.
      // You might need to add 'dateAdded' when saving places.
      filteredPlaces.value = [...savedPlaces.value].sort(
        (a, b) => new Date(b.dateAdded) - new Date(a.dateAdded)
      );
    };

    const confirmDeleteAllPlaces = async () => {
      toggleDeletePopup(); // Immediately hide the popup

      const cardContainers = document.querySelectorAll(".card-container");

      if (cardContainers.length > 0) {
        gsap.to(cardContainers, {
          opacity: 0,
          scale: 0.9,
          duration: 0.5,
          stagger: 0.1,
          onComplete: async () => {
            const user = getAuth().currentUser;
            if (user) {
              const userRef = doc(db, "users", user.uid);

              savedPlaces.value = [];
              filteredPlaces.value = [];

              try {
                await setDoc(userRef, { savedPlaces: [] }, { merge: true });
                console.log("All saved places deleted successfully.");
                showToast("Success", "All Places Deleted!", "remove");
              } catch (error) {
                console.error("Error deleting saved places:", error);
              }
            }
          },
        });
      } else {
        console.log("No cards to delete.");
      }
    };

    return {
      savedPlaces,
      filteredPlaces,
      loading,
      showModal,
      showDeletePopup,
      toggleItinerary,
      isPlaceInItinerary,
      toggleModal,
      removePlace,
      filterPlaces,
      confirmDeleteAllPlaces,
      toggleDeletePopup,
      navigateToGeneratedItinerary,
      itinerary,
      deleteAllPlaces,
      // Toast variables and functions
      progressBar,
      toastActive,
      toastTitle,
      toastMessage,
      toastType,
      showToast,
      closeToast,
    };
  },
};
</script>

<style scoped>
/* <================ HEADER CAROUSELL =================>*/

#carouselExampleInterval {
  position: relative;
  height: 550px;
  /* Fixed height */
  /* Set your desired height here */
  overflow: hidden;
}

.carousel-inner,
.gradientoverlay {
  height: 100%;
  /* Ensures inner elements match carousel height */
}

/* Main Itinerary Page */
.itinerary-page {
  margin: 0;
  padding: 0;
  background-color: #f0f6ff;
}

.gradientoverlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.2),
    rgba(0, 0, 0, 0.2)
  );
  /* Adjust gradient colors and opacity as desired */
  z-index: 1;
  /* Place it above the images but below the text */
}

.carousel-item {
  height: 100%;
  /* Ensures each item takes full height */
}

.carousel-item img {
  height: 100%;
  width: 100%;
  /* object-fit: cover; */
  /* Ensures the image covers the container without distorting */
}

.carousel-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  text-align: center;
  z-index: 2;
  /* Ensure it sits above the carousel images */
  width: 90%;
  /* Ensures text stays within bound at smaller screens */
}

.carousel-content h1 {
  font-size: 4.5rem;
  /* Adjust size as needed */
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
  /* Add spacing above the header */
  margin-bottom: 4rem;
  /* Add spacing below the header */
  text-align: left;
  /* Center align the text */
}

.secondary_content {
  padding: 0 60px;
}

.secondary_content h5 {
  color: rgb(166, 163, 163);
  margin-bottom: 1rem;
}

.form-select {
  background-color: #222;
  color: white;
  border: none;
  padding: 1rem 1.2rem;
  font-size: 1rem;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

/* Container to align dropdowns side by side */
.dropdown-container {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  margin-left: 60px;
  margin-right: 40px;

  /* Adjust this value to align the dropdowns with the text */
}

/* Style the dropdown button */
.dropdown-btn {
  background-color: #222;
  /* Dark background color */
  color: #fff;
  /* White text */
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  transition: background-color 0.3s ease;
  padding: 16px;
}

.dropdown-btn,
.form-select {
  width: 100%; /* Make all elements the same width */
  padding: 16px; /* Uniform padding */
  font-size: 1rem; /* Uniform font size */
  box-sizing: border-box; /* Include padding and border in the element’s total width and height */
}


/* Change button color on hover */
.dropdown-btn:hover {
  background-color: #555;
}

/* Dropdown content styling */
.dropdown-content {
  display: none;
  /* Hidden by default */
  position: absolute;
  background-color: #222;
  min-width: 200px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  border-radius: 5px;
  z-index: 1;
  top: 100%;
  /* Position below the button */
  left: 0;
  padding: 10px 0;
}

/* Dropdown content links */
.dropdown-content a {
  color: white;
  padding: 10px 20px;
  text-decoration: none;
  display: block;
  transition: background-color 0.3s ease;
}

/* Change background color on hover */
.dropdown-content a:hover {
  background-color: #333;
}

/* Show dropdown on hover */
.dropdown:hover .dropdown-content {
  display: block;
}

/* <=========== CARD GRID LAYOUT =============> */

.empty-message {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%; /* Adjust this if necessary */
  font-size: 1rem; /* Optional: to make the text more readable */
  color: #333; /* Optional: customize text color */
}

.transition-wrapper {
  display: contents;
  /* Keep the child elements visible */
  flex-wrap: wrap;
  /* Allow items to wrap */
  justify-content: flex-start;
  /* Align items to the start */
  gap: 15px;
  /* Optional: space between items */
  padding: 20px;
  /* Optional: padding around the grid */
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  /* Default to 3 items per row on large screens */
  gap: 1.5rem;
  /* Space between cards */
  row-gap: 4rem;
  padding: 2rem;
  /* Padding around the grid */
  margin-bottom: 50px;
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

/* Hover effect for cards */
.card-container:hover {
  transform: translateY(-4px);
  /* Moves the entire card upwards slightly */
  box-shadow: 0 8px 24px hsla(0, 0%, 0%, 0.2);
  /* Enhances shadow for lift effect */
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
  /* Text color for readability on image */
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  /* Slightly opaque black background */
  z-index: 1;
  /* Place between background image and text */
  border-radius: inherit;
}

.card-img-top {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-top-left-radius: 1.5rem;
  border-top-right-radius: 1.5rem;
  margin: 0;
}

.card-body {
  padding: 1rem;
  display: flex;
  font-family: "Source Sans 3", sans-serif;
  position: absolute;
  bottom: 0;
  left: 0.4;
  width: 100;
  flex-direction: column;
  align-items: flex-start;
  /* Align text to the left */
  border-bottom-left-radius: 1.5rem;
  border-bottom-right-radius: 1.5rem;
  z-index: 2;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  margin: 0;
  /* Remove any extra margins */
  text-align: left;
}

.card-text {
  font-size: 0.9rem;
  color: #eaeaea;
  margin-top: 0.3rem;
  /* Adjust spacing if needed */
  margin-left: 0;
  /* Adjust spacing if needed */
  margin-bottom: 0.3rem;
  text-align: left;
}

.rating-container {
  display: flex;
  align-items: center;
  gap: 5px; /* Adjust the spacing between items as needed */
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
  margin-bottom: 1rem;
}

.itinerary-button {
  background-color: #000000;
  color: white;
  width: 40%;
  /* Make the button full width */
  padding: 0.5rem 7rem;
  border-radius: 0.5rem;
  border: none;
  font-size: small;
  text-align: center;
  white-space: nowrap;
  /* Ensure text doesn’t wrap */
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: flex;
  /* Use flex to center the text */
  justify-content: center;
  /* Center text horizontally */
  align-items: center;
  /* Center text vertically */
}

.itinerary-button:hover {
  background-color: #004bb7;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  max-width: 500px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-image {
  width: 100%;
  height: auto;
  max-height: 150px;
  object-fit: cover;
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
  z-index: 1;
}

.close-button:hover {
  color: red;
}

.popup-container {
  position: fixed;
  left: 50%;
  bottom: 20px;
  transform: translateX(-50%);
  z-index: 2000;
}

.popup {
  background-color: #4caf50;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  transform: translateY(-5px);
}

.confirm-modal-btn {
  background-color: #ff4d4d; /* Red color similar to the second image */
  color: white;
  padding: 0.6rem 1.5rem;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 5px;
  transition: background-color 0.3s;
}

.close-modal-btn {
  background-color: #1e90ff; /* Blue color */
  color: white;
  padding: 0.6rem 1.5rem;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}


/* Toast Notification Styles */
.custom-toast {
  position: fixed;
  top: 25px;
  right: 35px;
  border-radius: 12px;
  background: #fff;
  /* Default background */
  padding: 20px 35px 20px 25px;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  border-left: 6px solid #007bff;
  /* Default border color */
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

/* Add Type Toast */
.custom-toast.add {
  /* Light green background */
  border-left-color: #28a745;
  /* Green border */
}

.custom-toast.add .action-icon {
  background-color: #28a745;
  /* Green icon background */
}

/* Remove Type Toast */
.custom-toast.remove {
  /* Light blue background */
  border-left-color: #17a2b8;
  /* Blue border */
}

.custom-toast.remove .action-icon {
  background-color: #17a2b8;
  /* Blue icon background */
}

/* Error Type Toast (Optional) */
.custom-toast.error {
  background: #fdecea;
  /* Light red background */
  border-left-color: #dc3545;
  /* Red border */
}

.custom-toast.error .action-icon {
  background-color: #dc3545;
  /* Red icon background */
}

.custom-toast .toast-content {
  display: flex;
  align-items: center;
}

.toast-content .action-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 35px;
  width: 35px;
  color: #fff;
  font-size: 20px;
  border-radius: 50%;
}

.toast-content .message {
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

.message .text.text-1 {
  font-weight: 600;
  color: #666;
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
  /* Start with scaleX(0) */
}

@keyframes progressBarAnimation {
  from {
    transform: scaleX(0);
  }

  to {
    transform: scaleX(1);
  }
}


/* <=========== BREAKPOINTS =============> */

/* Responsive adjustments */
@media (max-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
    /* 2 items per row on medium screens */
  }

  .sticky-top {
    padding: 0 3vw;
  }

  .overlay-text {
    font-size: 1.2rem;
  }

  .content h1 {
    font-size: 6rem;
  }

  .content h4 {
    font-size: 1.5rem;
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

@media (max-width: 767px) {
  .dropdown-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    /* 2x2 grid */
    gap: 1rem;
    /* Consistent gap between buttons */
  }

  .card-grid {
    grid-template-columns: 1fr;
    /* 1 item per row on small screens */
  }

  .sticky-top {
    padding: 0 2vw;
  }

  .overlay-text {
    font-size: 1rem;
  }

  .content h1 {
    font-size: 3rem;
  }

  .content h4 {
    font-size: 1.2rem;
  }

  .carousel-content h1 {
    font-size: 2rem;
  }

  .carousel-content h4 {
    font-size: 1rem;
  }
}

@media (max-width: 575px) {
  .dropdown-container {
    display: grid;
    grid-template-columns: 1fr;
    /* 2x2 grid */
    gap: 1rem;
    /* Consistent gap between buttons */
  }
} 


</style>
