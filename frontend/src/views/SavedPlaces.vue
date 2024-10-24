<template>
  <div class="itinerary-page">
    <div class="sticky-top">
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
          <button @click="toggleModal" type="button" class="btn btn-secondary view-itinerary-btn">View
            Itinerary</button>
          <button @click="navigateToGeneratedItinerary" type="button" class="btn btn-primary">View Full
            Itinerary</button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="empty-message">Loading saved places...</div>
    <div v-else-if="filteredPlaces && filteredPlaces.length === 0" class="empty-message">
      <p>No places saved yet.</p>
    </div>

    <div v-else class="card-grid">
      <transition-group name="list" tag="div" class="transition-wrapper">
        <div v-for="place in filteredPlaces" :key="place.place_id" class="card-container" ref="cardRefs">
          <div class="card destination-card">
            <button @click="removePlace(place)" type="button" class="btn close-button">X</button>
            <img :src="place.image" class="card-img-top" alt="Image of {{ place.name }}" />
            <div class="card-body">
              <h5 class="card-title">{{ place.name }}</h5>
              <p class="card-text">{{ place.vicinity }}, {{ place.country }}</p>
              <div class="button-container">
                <button @click="toggleItinerary(place, $event)" type="button" class="btn itinerary-button">
                  {{ isPlaceInItinerary(place) ? 'Remove from Itinerary' : 'Add to Itinerary' }}
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
          <li class="list-group-item" v-for="(item, index) in itinerary" :key="index">
            <img :src="item.image" class="modal-image" alt="Image of {{ item.name }}" />
            {{ item.name }} - {{ item.vicinity }}
          </li>
        </ol>
        <button @click="navigateToGeneratedItinerary" class="btn mb-2">View Full Itinerary</button>
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
import { ref, onMounted } from 'vue';
import { getFirestore, doc, getDoc, setDoc, updateDoc, arrayUnion, arrayRemove } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';
import { useRouter } from 'vue-router';
import { gsap } from "gsap";

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
    const cardRefs = ref([]); // Create a ref for card references

    // Fetching data from Firestore and storing it in savedPlaces
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

    // Save the itinerary list to Firebase
    const saveItinerary = async () => {
      const auth = getAuth();
      const user = auth.currentUser;
      const userId = user.uid;
      const userRef = doc(db, "users", userId);
      try {
        await setDoc(
          userRef,
          { generatedItinerary: [...itinerary.value] },
          { merge: true }
        );
      } catch (error) {
        console.error("Error saving itinerary:", error);
      }
    };

    const navigateToGeneratedItinerary = () => {
      router.push({
        name: 'MyItineraries',
      });
    };

    const isPlaceInItinerary = (place) => {
      return itinerary.value.some(item => item.place_id === place.place_id);
    };

    const deleteAllPlaces = async () => {
      toggleDeletePopup(); // Show delete confirmation popup
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

    const toggleItinerary = async (place, event) => {
      const index = savedPlaces.value.findIndex(item => item.place_id === place.place_id);

      if (index !== -1) {
        const user = getAuth().currentUser;

        if (!user) {
          console.error('User is not authenticated');
          return;
        }

        const userId = user.uid;
        const userDocRef = doc(db, 'users', userId);

        try {
          const placeData = {
            place_id: place.place_id,
            name: place.name,
            image: place.image,
            vicinity: place.vicinity,
            country: place.country,
            coordinates: {
              latitude: place.coordinates.latitude,   // Include latitude
              longitude: place.coordinates.longitude   // Include longitude
            }
          };

          if (isPlaceInItinerary(place)) {
            await updateDoc(userDocRef, {
              generatedItineraries: arrayRemove(placeData)
            });

            itinerary.value = itinerary.value.filter(item => item.place_id !== place.place_id);
            togglePopup('remove');
          } else {
            const button = event.currentTarget;

            gsap.fromTo(
              button,
              { scale: 1 },
              {
                scale: 1.1,
                duration: 0.2,
                yoyo: true,
                repeat: 1
              }
            );

            await updateDoc(userDocRef, {
              generatedItineraries: arrayUnion(placeData)
            });

            itinerary.value.push({ ...place });
            togglePopup('add');
          }
        } catch (error) {
          console.error('Error updating itinerary in Firebase:', error);
        }
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
            const userDocRef = doc(db, 'users', userId);

            const userDoc = await getDoc(userDocRef);
            if (userDoc.exists()) {
              const data = userDoc.data().generatedItineraries;
              itinerary.value = data || [];
            } else {
              console.log('No document found for the user.');
            }
          } else {
            console.error('User is not authenticated.');
          }
        } catch (error) {
          console.error('Error fetching generatedItineraries from Firebase:', error);
        }
      }
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
      filteredPlaces.value = [...savedPlaces.value].sort((a, b) => new Date(b.dateAdded) - new Date(a.dateAdded));
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
              } catch (error) {
                console.error("Error deleting saved places:", error);
              }
            }
          }
        });
      } else {
        console.log("No cards to delete.");
      }
    };

    const addPlaceToItinerary = async (place) => {
      itinerary.value.push(place);

      const user = getAuth().currentUser;
      const userEmail = user.email;
      const userDocRef = doc(db, 'users', userEmail);

      try {
        await updateDoc(userDocRef, {
          generatedItineraries: arrayUnion({
            place_id: place.place_id,
            name: place.name,
            image: place.image,
            vicinity: place.vicinity,
            country: place.country,
            coordinates: {
              latitude: place.coordinates.latitude,   // Include latitude
              longitude: place.coordinates.longitude   // Include longitude
            }
          })
        });
      } catch (error) {
        console.error("Error updating itinerary in Firebase:", error);
      }
    };


    return {
      savedPlaces,
      addPlaceToItinerary,
      filteredPlaces,
      loading,
      toggleItinerary,
      isPlaceInItinerary,
      toggleModal,
      removePlace,
      filterPlaces,
      confirmDeleteAllPlaces,
      toggleDeletePopup,
      navigateToGeneratedItinerary,
      itinerary,
      showPopup,
      showRemovePopup,
      showModal,
      showDeletePopup,
      deleteAllPlaces,
      saveItinerary,
      cardRefs, // Return cardRefs for use in the template
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
}

.modal-image {
  width: 100%;
  height: auto;
  max-height: 150px;
  /* Keep the height consistent */
  object-fit: cover;
}

/* Other styles remain unchanged */

.card-container {
  flex: 0 0 auto;
  /* Fixed width for the cards, they won't grow */
  max-width: 265px;
  /* Ensures the cards stay at 265px */
  min-width: 265px;
  /* Ensures the cards stay at 265px */
  margin: 0px;
  /* Adds spacing between cards */
}

.card-grid {
  display: flex;
  flex-wrap: wrap;
  /* Allows cards to wrap onto the next row */
  justify-content: center;
  /* Align the cards to the left */
  gap: 17px;
  /* Space between cards */
}

.card {
  display: flex;
  flex-direction: column;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.destination-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  /* Ensures the button is at the bottom */
  height: 450px;
  /* Set the fixed height for all cards */
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
  display: flex;
  justify-content: center;
  /* Center the button horizontally */
  margin-top: auto;
  /* Pushes the button to the bottom */
}

.itinerary-button {
  width: 100%;
  /* Makes the button take the full width */
  padding: 10px;
  /* Add some padding for a larger clickable area */
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
  transform: translateY(-5px);
  /* Lift effect on hover */
}

.itinerary-page {
  font-family: "Roboto", sans-serif;
  margin: 0;
  padding: 0;
}


.sticky-top {
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

.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter,
.list-leave-to

/* .list-leave-active in <2.1.8 */
  {
  opacity: 0;
  transform: translateY(30px);
}

.list-move {
  transition: transform 0.5s ease;
}

.transition-wrapper {
  display: flex;
  /* Ensure that transition group behaves like flexbox */
  flex-wrap: wrap;
  /* Allow items to wrap */
  justify-content: flex-start;
  /* Align items to the start */
  gap: 15px;
  /* Optional: space between items */
  padding: 20px;
  /* Optional: padding around the grid */
}
</style>
