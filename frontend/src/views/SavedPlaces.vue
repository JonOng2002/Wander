<template>
  <div class="itinerary-page">
    <AppNavbar class="sticky-top"></AppNavbar>
    <div class="row justify-content-between align-items-center sticky-header g-0">
      <div class="col-3 date-column">
        <h2>My Saved Places</h2>
        <div class="filter-dropdown d-flex align-items-center">
          <select @change="filterPlaces" class="form-select me-2">
            <option value="">Select Filter</option>
            <option value="alphabetical">Filter by Alphabet</option>
            <option value="recently-added">Filter by Recently Added</option>
          </select>
          <button @click="deleteAllPlaces" :disabled="isDeleteAllDisabled" class="btn btn-delete-all">
            Delete All
          </button>
        </div>
      </div>
      <div class="col-auto generateButton">
        <button @click="toggleModal" type="button" class="btn btn-secondary view-itinerary-btn">View Itinerary</button>
        <button @click="navigateToGeneratedItinerary" type="button" class="btn btn-primary">Generate Itinerary!</button>
      </div>
    </div>

    <div v-if="loading" class="empty-message">Loading saved places...</div>
    <div v-else-if="filteredPlaces && filteredPlaces.length === 0" class="empty-message">
      <p>No places saved yet.</p>
    </div>

    <div v-else class="card-grid">
      <transition-group name="list" tag="div" class="transition-wrapper">
        <div v-for="place in filteredPlaces" :key="place.place_id" class="card-container">
          <div class="card destination-card">
            <!-- Close Button -->
            <button @click="removePlace(place)" type="button" class="btn close-button">X</button>

            <img :src="place.image" class="card-img-top" alt="Image of {{ place.name }}" />
            <div class="card-body">
              <h5 class="card-title">{{ place.name }}</h5>
              <p class="card-text">{{ place.vicinity }}, {{ place.country }}</p>
              <div class="button-container">
                <button @click="toggleItinerary(place)" type="button" class="btn itinerary-button">
                  {{ isPlaceInItinerary(place) ? 'Remove from Itinerary' : 'Add to Itinerary' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </transition-group>
    </div>

    <!-- Modal structure -->
    <div v-if="showModal" class="modal-overlay" @click.self="toggleModal">
      <div class="modal-content">
        <h3>Your Itinerary</h3>
        <ol class="list-group list-group-numbered">
          <li class="list-group-item" v-for="(item, index) in itinerary" :key="index">
            <img :src="item.image" class="modal-image" alt="Image of {{ item.name }}" />
            {{ item.name }} - {{ item.vicinity }}
          </li>
        </ol>
        <button @click="toggleModal" type="button" class="btn close-modal-btn">Close</button>
      </div>
    </div>

    <div v-if="showDeletePopup" class="modal-overlay" @click.self="toggleDeletePopup">
      <div class="modal-content">
        <h3>Are you sure you want to delete all saved places?</h3>
        <button @click="confirmDeleteAllPlaces" type="button" class="btn mb-2">Yes, Delete All</button>
        <button @click="toggleDeletePopup" type="button" class="btn close-modal-btn">Cancel</button>
      </div>
    </div>

    <div class="popup-container">
      <div v-if="showPopup" class="popup">
        <p>Added to itinerary!</p>
      </div>

      <div v-if="showRemovePopup" class="popup" style="background-color: #f44336;">
        <p>Removed from itinerary!</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { getFirestore, doc, getDoc, setDoc } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';
import { useRouter } from 'vue-router';
import AppNavbar from '@/components/AppNavbar.vue';

export default {
  name: 'SavedPlaces',
  setup() {
    const savedPlaces = ref([]);
    const filteredPlaces = ref([]);
    const itinerary = ref([]);
    const loading = ref(true);
    const showPopup = ref(false);
    const showRemovePopup = ref(false);
    const showModal = ref(false);
    const showDeletePopup = ref(false);
    const db = getFirestore();
    const router = useRouter();

    onMounted(async () => {
      const auth = getAuth();
      const user = auth.currentUser;

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

    const navigateToGeneratedItinerary = () => {
      router.push({ name: 'GeneratedItinerary' });
    };

    const isPlaceInItinerary = (place) => {
      return itinerary.value.some(item => item.place_id === place.place_id);
    };

    const togglePopup = (type) => {
      if (type === 'add') {
        showPopup.value = true;
        setTimeout(() => {
          showPopup.value = false;
        }, 2000);
      } else if (type === 'remove') {
        showRemovePopup.value = true;
        setTimeout(() => {
          showRemovePopup.value = false;
        }, 2000);
      }
    };

    const toggleDeletePopup = () => {
      showDeletePopup.value = !showDeletePopup.value; // Toggle delete confirmation popup
    };

    const toggleItinerary = (place) => {
      if (isPlaceInItinerary(place)) {
        itinerary.value = itinerary.value.filter(item => item.place_id !== place.place_id);
        togglePopup('remove');
      } else {
        itinerary.value.push(place);
        togglePopup('add');
      }
    };

    const toggleModal = () => {
      showModal.value = !showModal.value;
    };

    const removePlace = (place) => {
      const index = savedPlaces.value.findIndex(item => item.place_id === place.place_id);
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
              togglePopup('remove');
            })
            .catch((error) => {
              console.error("Error updating Firestore:", error);
            });
        }
      } else {
        console.log("Place not found in saved places.");
      }
    };

    const filterPlaces = (event) => {
      const value = event.target.value;
      if (value === 'alphabetical') {
        filterAlphabetically();
      } else if (value === 'recently-added') {
        filterRecentlyAdded();
      } else {
        filteredPlaces.value = [...savedPlaces.value];
      }
    };

    const filterAlphabetically = () => {
      filteredPlaces.value = [...savedPlaces.value].sort((a, b) => a.name.localeCompare(b.name));
    };

    const filterRecentlyAdded = () => {
      filteredPlaces.value = [...savedPlaces.value].sort((a, b) => b.timestamp - a.timestamp);
    };



    // Update the deleteAllPlaces method to confirm deletion
    const deleteAllPlaces = async () => {
      toggleDeletePopup(); // Show delete confirmation popup
    };

    // Confirm deletion of all places
    const confirmDeleteAllPlaces = async () => {
      const user = getAuth().currentUser;
      if (user) {
        const userRef = doc(db, "users", user.uid);

        savedPlaces.value = [];
        filteredPlaces.value = [];

        try {
          await setDoc(userRef, { savedPlaces: [] }, { merge: true });
          console.log("All saved places deleted successfully.");
          toggleDeletePopup(); // Close the delete confirmation popup
        } catch (error) {
          console.error("Error deleting saved places:", error);
        }
      }
    };

    // Computed property to check if delete all button should be disabled
    const isDeleteAllDisabled = computed(() => {
      return savedPlaces.value.length === 0; // Disable button if savedPlaces is empty
    });

    return {
      savedPlaces,
      filteredPlaces,
      itinerary,
      loading,
      showPopup,
      showRemovePopup,
      showModal,
      showDeletePopup,
      isDeleteAllDisabled, // Expose the computed property
      navigateToGeneratedItinerary,
      toggleItinerary,
      toggleModal,
      isPlaceInItinerary,
      removePlace,
      filterPlaces,
      deleteAllPlaces,
      confirmDeleteAllPlaces,
      toggleDeletePopup,
      AppNavbar
    };
  },
};
</script>


<style scoped>
h2 {
  font-family: 'Cormorant Garamond', serif;
  font-weight: bolder;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  /* Keep the modal overlay fixed */
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  /* Dark background for the overlay */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  /* High enough to overlap the navbar */
}


.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  max-width: 500px;
  width: 100%;
  max-height: 80vh;
  /* Set a maximum height */
  overflow-y: auto;
  /* Enable vertical scrolling */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  position: relative;
}

.modal-image {
  width: 100%;
  height: auto;
  max-height: 150px;
  /* Keep the height consistent */
  object-fit: cover;
}

/* Other styles remain unchanged */

.card-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  gap: 15px;
  padding: 20px;
}

.card-container {
  flex: 0 0 auto;
  max-width: 265px;
  width: 100%;
}

.card {
  display: flex;
  flex-direction: column;
  height: 100%;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}



.destination-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Ensures the button is at the bottom */
  height: 400px; /* Set the fixed height for all cards */
  padding: 10px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}


.card-body {
  flex-grow: 1;
  padding: 10px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.button-container {
  position: relative;
  margin-top: 10px; /* Ensures there is space between the content and the button */
  display: flex;
  justify-content: center; /* Center the button horizontally */
}

.itinerary-button {
  width: 100%; /* Makes the button take the full width */
  padding: 10px; /* Add some padding for a larger clickable area */
}


.destination-card:hover {
  transform: translateY(-5px);
  /* Lift effect on hover */
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  /* Enhanced shadow with darker effect */
}


.card-img-top {
  width: 100%;
  height: 200px;
  /* Fixed height for consistency */
  object-fit: cover;
}

.card-body {
  padding: 10px;
}

.btn {
  background-color: black;
  /* Set button color to black */
  color: white;
  /* Keep the text color white for contrast */
  border: none;
  /* Remove default border */
}

.btn:hover {
  background-color: #333;
  /* Darker color on hover for visual feedback */
  color: white;
  /* Keep the text color white on hover */
}

.close-modal-btn:hover {
  background-color: #333;
  /* Darker color on hover for the close button */
  color: white;
  /* Keep the text color white on hover */
}

.view-itinerary-btn {
  margin-right: 10px;
  /* Adjust space as needed */
}

.popup-container {
  position: fixed;
  /* Fixed position to stay at the bottom */
  left: 50%;
  /* Center horizontally */
  bottom: 20px;
  /* Space from the bottom */
  transform: translateX(-50%);
  /* Adjust centering */
  z-index: 2000;
  /* Ensure it appears above other elements */
}

.popup {
  background-color: #4caf50;
  /* Green for added */
  color: white;
  /* Text color */
  padding: 10px 20px;
  /* Padding */
  border-radius: 5px;
  /* Rounded corners */
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  /* Enhanced shadow with darker effect */
  /* Shadow effect */
  /* transition: opacity 0.3s ease; */
  /* Transition for fading effects */
  transform: translateY(-5px);
  /* Lift effect on hover */
}


.itinerary-page {
  font-family: "Roboto", sans-serif;
  margin: 0;
  padding: 0;
}

.sticky-top {
  top: 0;
  position: sticky;
  z-index: 1020; /* Higher z-index to ensure navbar stays above other elements */
  background-color: black; /* Ensure the background remains black */
}

.content {
  padding: 20px;
  /* Ensure enough space for scrolling */
  min-height: 150vh; /* Adjust as needed for testing */
}

.sticky-header {
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 1000;
  padding: 10px 5%;
  border-bottom: 1px solid lightgrey;
}

.date-column {
  text-align: left;
  padding-left: 15px;
  /* Increase padding to move it left */
  font-family: 'Roboto', sans-serif;
  /* Change to your desired font */
  font-size: 1.5rem;
  /* Adjust font size if necessary */
  margin-top: 10px;
  margin-bottom: 10px;
}

.generateButton {
  text-align: right;
  padding-right: 5%;
  font-size: 1.5rem;
  margin-top: 10px;
  margin-bottom: 10px;
}

.empty-message {
  text-align: center;
  font-size: 1.2rem;
  color: grey;
  margin-top: 20px;
}

.close-button {
  position: absolute;
  top: 10px;
  /* Adjust as needed */
  right: 10px;
  /* Adjust as needed */
  background: transparent;
  /* No background */
  border: none;
  /* No border */
  color: white;
  /* Color of the 'X' */
  font-size: 1.2rem;
  /* Adjust size */
  cursor: pointer;
  /* Pointer cursor */
  z-index: 1;
  /* Ensure it is on top */
}

.close-button:hover {
  color: white;
  /* Change color on hover */
}

.filter-dropdown {
  margin: 10px 0;
}

.filter-dropdown .form-select {
  width: 100%;
}

.btn-delete-all {
  width: 150px;
}

.list-enter-active, .list-leave-active {
  transition: all 0.5s ease;
}
.list-enter, .list-leave-to /* .list-leave-active in <2.1.8 */ {
  opacity: 0;
  transform: translateY(30px);
}
.list-move {
  transition: transform 0.5s ease;
}

.transition-wrapper {
  display: flex;        /* Ensure that transition group behaves like flexbox */
  flex-wrap: wrap;     /* Allow items to wrap */
  justify-content: flex-start; /* Align items to the start */
  gap: 15px;           /* Optional: space between items */
  padding: 20px;       /* Optional: padding around the grid */
}

</style>