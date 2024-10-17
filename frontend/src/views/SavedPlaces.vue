<template>
  <div class="itinerary-page">
    <div class="row justify-content-between align-items-center sticky-header g-0 m-2">
      <!-- Date Column -->
      <div class="col-3 date-column">
        <h2>My Saved Places</h2>
      </div>
      <!-- Generate Itinerary Button -->
      <div class="col-auto generateButton">
        <button @click="navigateToGeneratedItinerary" type="button" class="btn btn-primary">Generate Itinerary!</button>
      </div>
    </div>

    <!-- Loading indicator -->
    <div v-if="loading" class="empty-message">Loading saved places...</div>

    <!-- No places saved message -->
    <div v-else-if="savedPlaces && savedPlaces.length === 0" class="empty-message">
      <p>No places saved yet.</p>
    </div>

    <!-- Display saved places -->
    <div v-else class="row card-row justify-content-start g-0">
      <div v-for="place in savedPlaces" :key="place.place_id" class="card-container">
        <div class="card destination-card">
          <img :src="place.image" class="card-img-side" alt="Image of {{ place.name }}" />
          <div class="card-body">
            <h5 class="card-title">{{ place.name }}</h5>
            <p class="card-text">{{ place.vicinity }}, {{ place.country }}</p>

            <p>
              <button @click="addToItinerary(place)" type="button" id="addToItinerary" class="btn">
                Add to Itinerary
              </button>
            </p>

            <!-- Remove from saved places button-->
            <p>
              <button @click="removeFromSavedPlaces(place.place_id)" type="button" class="btn btn-danger">
                Remove
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Itinerary List Display -->
    <div v-if="itinerary.length > 0" class="itinerary-list">
      <h3>Your Itinerary</h3>
      <ol class="list-group list-group-numbered">
        <li class="list-group-item" v-for="(item, index) in itinerary" :key="index">
          {{ item.name }} - {{ item.vicinity }}
        </li>
      </ol>
    </div>

    <!-- Popup notification -->
    <div v-if="showPopup" class="popup">
      <p>Added to itinerary!</p>
    </div>
  </div>

  <!-- Remove Popup notification -->
  <div v-if="showRemovePopup" class="popup" style="background-color: #f44336;">
    <p>Removed from itinerary!</p>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { getFirestore, doc, getDoc, updateDoc, arrayRemove } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';
import { useRouter } from 'vue-router';


export default {
  name: 'SavedPlaces',
  setup() {
    const savedPlaces = ref([]);
    const itinerary = ref([]);
    const loading = ref(true);
    const showPopup = ref(false);
    const showRemovePopup = ref(false);
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

    const addToItinerary = (place) => {
      const isAlreadyInItinerary = itinerary.value.some(item => item.place_id === place.place_id);
      if (!isAlreadyInItinerary) {
        itinerary.value.push(place);
        showPopup.value = true;
        setTimeout(() => {
          showPopup.value = false;
        }, 2000);
      } else {
        console.log(`${place.name} is already in the itinerary`);
      }
    };

    const removeFromSavedPlaces = async (placeId) => {
      const auth = getAuth();
      const user = auth.currentUser;

      if (user) {
        const userId = user.uid;
        const userRef = doc(db, "users", userId);

        try {
          // Find the place in the local savedPlaces array
          const placeToRemove = savedPlaces.value.find(place => place.place_id === placeId);

          // Remove the place from Firebase using arrayRemove
          if (placeToRemove) {
            await updateDoc(userRef, {
              savedPlaces: arrayRemove(placeToRemove)
            });

            // Update the local state after successful Firebase update
            savedPlaces.value = savedPlaces.value.filter(place => place.place_id !== placeId);
            itinerary.value = itinerary.value.filter(item => item.place_id !== placeId);

            showRemovePopup.value = true;
            setTimeout(() => {
              showRemovePopup.value = false;
            }, 2000); 
          }
        } catch (error) {
          console.error("Error removing place from Firebase:", error);
        }
      } else {
        console.error("User is not authenticated");
      }
    };

    return {
      savedPlaces,
      itinerary,
      loading,
      showPopup,
      showRemovePopup,
      navigateToGeneratedItinerary,
      addToItinerary,
      removeFromSavedPlaces,
    };
  },
};
</script>


<style scoped>
.itinerary-page {
  font-family: "Roboto", sans-serif;
  margin: 0;
  padding: 0;
}

/* Ensure the header is sticky */
.sticky-header {
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 1000;
  padding: 10px 5%;
  border-bottom: 1px solid lightgrey;
}

/* Ensure the date column is pushed to the left */
.date-column {
  text-align: left;
  padding-left: 5%;
  padding-right: 0;
  white-space: nowrap;
  font-size: 1.5rem;
  margin-top: 10px;
  margin-bottom: 10px;
}

.generateButton {
  text-align: right;
  padding-right: 5%;
  padding-left: 0;
  white-space: nowrap;
  font-size: 1.5rem;
  margin-top: 10px;
  margin-bottom: 10px;
}

/* Empty message styles */
.empty-message {
  text-align: center;
  font-size: 1.2rem;
  color: gray;
  padding: 20px;
}

/* Reset or minimize row margin */
.row {
  margin-left: 0 !important;
  margin-right: 0 !important;
  margin-top: 3%;
}

.card-row {
  margin-top: 10px;
}

/* card container styles */
.card-container {
  padding-left: 5%;
  padding-right: 5%;
  margin-bottom: 10px;
}

/* card styles */
.destination-card {
  margin-left: 0;
  padding: 15px;
  height: auto;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  flex-direction: row;
  overflow: hidden;
  border-radius: 10px;
}

.card-img-side {
  width: 250px;
  max-height: 200px;
  object-fit: cover;
  margin-right: 15px;
}

.card-body {
  flex-grow: 1;
}

.card-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.card-text {
  font-size: 1rem;
  line-height: 1.4;
}

.btn {
  background-color: lightgray;
  color: black;
  border: 1px solid black;
}

.btn:hover {
  background-color: darkgray;
  color: black;
}

/* Popup notification styles */
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

.remove-popup {
  background-color: #f44336; /* Red background for remove popup */
}

/* Itinerary list styles */
.itinerary-list {
  margin-top: 20px;
}

.itinerary-list h3 {
  text-align: center;
}

.itinerary-list ul {
  list-style: none;
  padding: 0;
}

.itinerary-list li {
  margin: 10px 0;
  font-size: 1.2rem;
  text-align: center;
}
</style>
