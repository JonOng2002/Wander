<template>
  <div id="carouselExampleInterval" class="carousel slide" data-bs-ride="carousel">
    <div class="carousel-inner">
      <div class="carousel-item active" data-bs-interval="10000">
        <img src="@/assets/countries/thailand.jpg" alt="Image 1" class="d-block w-100" />
      </div>
      <div class="carousel-item" data-bs-interval="2000">
        <img src="@/assets/countries/denmark.jpg" alt="Image 1" class="d-block w-100" />
      </div>
      <div class="carousel-item">
        <img src="@/assets/countries/germany.jpg" alt="Image 1" class="d-block w-100" />
      </div>
    </div>

    <!-- Gradient Overlay -->
    <div class="gradientoverlay"></div>

    <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleInterval" data-bs-slide="prev">
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleInterval" data-bs-slide="next">
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
          <option value="">Select Filter</option>
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
  <div v-else-if="filteredPlaces && filteredPlaces.length === 0" class="empty-message">
    <p>No places saved yet.</p>
  </div>

  <div v-else class="card-grid">
    <transition-group name="list" tag="div" class="transition-wrapper">
      <div v-for="place in filteredPlaces" :key="place.place_id" class="card-container" ref="cardRefs" v-motion-slide-visible-once-top>
        <div class="card destination-card" :style="{ backgroundImage: `url(${place.image})` }">
          <div class="overlay"></div>
          <button @click="removePlace(place)" type="button" class="btn close-button">✖</button>
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
      <button @click="navigateToGeneratedItinerary" class="btn mb-2 view-full-itinerary-btn">View Full
        Itinerary</button>
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
      loadUserItinerary();

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

    console.log(savedPlaces);


    //save itinerary to firestore
    const saveItinerary = async (place) => {
      console.log('start saving itinerary');
      console.log(itinerary.value);
      const auth = getAuth();
      const user = auth.currentUser;

      if (!user) {
        console.error("User is not authenticated");
        return;
      }

      const userDocRef = doc(db, "users", user.uid);
      const placeData = {
        place_id: place.place_id,
        name: place.name,
        image: place.image,
        vicinity: place.vicinity,
        country: place.country,
        coordinates: {
          latitude: place.coordinates.latitude,
          longitude: place.coordinates.longitude,
        },
      };

      try {
        if (isPlaceInItinerary(place)) {
          // Remove place from itinerary in Firebase
          await updateDoc(userDocRef, {
            generatedItineraries: arrayRemove(placeData),
          });
          itinerary.value = itinerary.value.filter(item => item.place_id !== place.place_id);
          console.log("Place removed from itinerary:", placeData);
          togglePopup("remove");
        } else {
          // Add place to itinerary in Firebase
          await updateDoc(userDocRef, {
            generatedItineraries: arrayUnion(placeData),
          });
          itinerary.value.push(place);
          console.log("Place added to itinerary:", placeData);
          togglePopup("add");
        }
      } catch (error) {
        console.error("Error updating itinerary in Firebase:", error);
      }
    };

    const navigateToGeneratedItinerary = () => {
      router.push({
        name: 'ItineraryBuilder',
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

    const loadUserItinerary = async () => {
      const user = getAuth().currentUser;

      if (user) {
        const userId = user.uid;
        const userDocRef = doc(db, 'users', userId);

        try {
          const docSnap = await getDoc(userDocRef);
          if (docSnap.exists()) {
            itinerary.value = docSnap.data().generatedItineraries || [];
            // Update the state for each place based on loaded itinerary
          } else {
            console.error('No such document!');
          }
        } catch (error) {
          console.error('Error fetching user itinerary:', error);
        }
      }
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

          const isInItinerary = isPlaceInItinerary(place);  // Check if the place is in the itinerary

          // Immediate local state update for reactivity
          if (isInItinerary) {
            // Remove from itinerary locally first
            itinerary.value = itinerary.value.filter(item => item.place_id !== place.place_id);
            togglePopup('remove');  // Show remove popup

            // Update Firebase after local state change
            await updateDoc(userDocRef, {
              generatedItineraries: arrayRemove(placeData)
            });
          } else {
            const button = event.currentTarget;

            // GSAP animation for button
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

            // Add to itinerary locally first
            itinerary.value.push({ ...place });
            togglePopup('add');  // Show add popup

            // Update Firebase after local state change
            await updateDoc(userDocRef, {
              generatedItineraries: arrayUnion(placeData)
            });
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
      showPopup,
      showRemovePopup,
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
      saveItinerary,
      cardRefs, // Return cardRefs for use in the template
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

.gradientoverlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.2));
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
  background: rgba(0, 0, 0, 0.0);
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
  background-color: rgba(0, 0, 0, 0.2);
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
  cursor: pointer;
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
  background: rgba(0, 0, 0, 0.7);
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

@media (max-width: 768px) {
  .dropdown-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr); /* 2x2 grid */
    gap: 1rem; /* Consistent gap between buttons */
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

@media (max-width: 576px) {
  .dropdown-container {
    display: flex;
    flex-direction: column;
    gap: 1rem; /* Consistent gap between buttons */
  }

  .sticky-top {
    padding: 0 1.5vw;
  }
}
</style>
