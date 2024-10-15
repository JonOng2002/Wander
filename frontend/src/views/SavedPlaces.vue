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

    <!-- List of saved places -->
    <div v-if="savedPlaces.length === 0" class="empty-message">
      <p>No places saved yet.</p>
    </div>

    <div v-else class="row card-row justify-content-start g-0">
      <div v-for="place in savedPlaces" :key="place.place_id" class="card-container">
        <div class="card destination-card">
          <img :src="place.image" class="card-img-side" alt="place-image" />
          <div class="card-body">
            <h5 class="card-title">{{ place.name }}</h5>
            <p class="card-text">{{ place.vicinity }}</p>

            <p><button @click="addToItinerary(place)" type="button" id="addToItinerary" class="btn">Add to Itinerary</button></p>
            
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

    <!-- Popup notification -->
    <div v-if="showPopup" class="popup">
      <p>Added to itinerary!</p>
    </div>

    <!-- Itinerary list -->
    <div v-if="itinerary.length > 0" class="itinerary-list">
      <h3>Your Itinerary</h3>
      <ol class="list-group list-group-numbered">
        <li class="list-group-item" v-for="(item, index) in itinerary" :key="index">
          {{ item.name }} - {{ item.vicinity }}
        </li>
      </ol>
    </div>
  </div>
</template>

<script>
export default {
  name: "SavedPlaces",
  inject: ['savedPlacesState', 'itineraryState'], // Inject the saved places and itinerary state 
  data() {
    return {
      
      showPopup: false, // To show the 'Added to itinerary' popup
    };
  },
  computed: {
    savedPlaces() {
      console.log(this.savedPlacesState);

      return this.savedPlacesState.savedPlaces; // Retrieve saved places from the global state
    },

    itinerary() {
      return this.itineraryState.itinerary; // Retrieve itinerary from the global state
    }
  },
  methods: {
    navigateToGeneratedItinerary() {
      this.$router.push({ name: 'GeneratedItinerary' });
    },
    addToItinerary(place) {
      this.itinerary.push(place); // Add the place to the itinerary list

      // Show popup notification
      this.showPopup = true;
      setTimeout(() => {
        this.showPopup = false; // Hide popup after 2 seconds
      }, 2000);
    },
    removeFromSavedPlaces(placeId) {
      this.savedPlacesState.removePlace(placeId); // Call removePlace from global state

      // Also remove from itinerary if it exists
      const indexInItinerary = this.itinerary.findIndex(item => item.place_id === placeId);
      if (indexInItinerary !== -1) {
        this.itinerary.splice(indexInItinerary, 1); // Remove from itinerary array
      }
    },
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
  background-color: darkgray; /* Slightly change color, but don't fade it out */
  color: black; /* Keep text color consistent */
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
