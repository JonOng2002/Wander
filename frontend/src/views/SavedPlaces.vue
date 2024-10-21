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
            <button @click="removePlace(place)" type="button" class="btn close-button">X</button>
            <img :src="place.image" class="card-img-top" :alt="'Image of ' + place.name" />
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
    <transition name="modal">
      <div v-if="showModal" class="modal-overlay" @click.self="toggleModal">
        <div class="modal-content">
          <h3>Your Itinerary</h3>
          <ol class="list-group list-group-numbered">
            <li class="list-group-item" v-for="item in itinerary" :key="item.place_id"> <!-- Removed unused 'index' -->
              <img :src="item.image" class="modal-image" :alt="'Image of ' + item.name" />
              {{ item.name }} - {{ item.vicinity }}
            </li>
          </ol>
          <button @click="toggleModal" type="button" class="btn close-modal-btn">Close</button>
        </div>
      </div>
    </transition>

    <!-- Delete confirmation modal -->
    <transition name="modal">
      <div v-if="showDeletePopup" class="modal-overlay" @click.self="toggleDeletePopup">
        <div class="modal-content">
          <h3>Are you sure you want to delete all saved places?</h3>
          <button @click="confirmDeleteAllPlaces" type="button" class="btn mb-2">Yes, Delete All</button>
          <button @click="toggleDeletePopup" type="button" class="btn close-modal-btn">Cancel</button>
        </div>
      </div>
    </transition>

    <div class="popup-container">
      <transition name="popup-fade">
        <div v-if="showPopup" class="popup">
          <p>Added to itinerary!</p>
        </div>
      </transition>
      <transition name="popup-fade">
        <div v-if="showRemovePopup" class="popup" style="background-color: #f44336;">
          <p>Removed from itinerary!</p>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, computed } from 'vue';
import { getFirestore, doc, getDoc, setDoc } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';
import { useRouter } from 'vue-router';
import AppNavbar from '@/components/AppNavbar.vue';

export default {
  name: 'SavedPlaces',
  components: {
    AppNavbar
  },
  setup() {
    const savedPlaces = ref([]);
    const filteredPlaces = ref([]);
    const itinerary = ref([]);
    const loading = ref(true);
    const showPopup = ref(false);
    const showRemovePopup = ref(false);
    const showModal = ref(false);
    const showDeletePopup = ref(false);
    const visibleCards = ref([]);  // Initialize visibleCards
    const initialRender = ref(true);  // Initialize initialRender
    const db = getFirestore();
    const router = useRouter();

    onMounted(async () => {
      const auth = getAuth();
      const user = auth.currentUser;

      if (user) {
        const userId = user.uid;
        const userRef = doc(db, 'users', userId);

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
          console.error('Error fetching saved places:', error);
        } finally {
          loading.value = false;
        }

        nextTick(() => {
          observeCards();
          // Start showing cards with a delay
          setTimeout(() => {
            savedPlaces.value.forEach((place, index) => {
              setTimeout(() => {
                visibleCards.value.push(place.place_id);  // Fixed: visibleCards now defined
              }, index * 200);
            });
            setTimeout(() => {
              initialRender.value = false;  // Fixed: initialRender now defined
            }, savedPlaces.value.length * 200);
          }, 100);
        });
      } else {
        console.error('User is not authenticated');
        loading.value = false;
      }
    });

    const observeCards = () => {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const cardId = entry.target.dataset.id;
            if (!visibleCards.value.includes(cardId)) {  // Fixed: visibleCards now defined
              visibleCards.value.push(cardId);  // Fixed: visibleCards now defined
            }
          }
        });
      });

      const cardElements = document.querySelectorAll('.card-container');
      cardElements.forEach((card) => {
        observer.observe(card);
      });
    };

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
      showDeletePopup.value = !showDeletePopup.value;
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
          const userRef = doc(db, 'users', userId);

          setDoc(userRef, { savedPlaces: savedPlaces.value }, { merge: true })
            .then(() => {
              togglePopup('remove');
            })
            .catch((error) => {
              console.error('Error updating Firestore:', error);
            });
        }
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

    const deleteAllPlaces = () => {
      toggleDeletePopup();
    };

    const confirmDeleteAllPlaces = async () => {
      const user = getAuth().currentUser;
      if (user) {
        const userRef = doc(db, 'users', user.uid);
        savedPlaces.value = [];
        filteredPlaces.value = [];
        try {
          await setDoc(userRef, { savedPlaces: [] }, { merge: true });
          toggleDeletePopup();
        } catch (error) {
          console.error('Error deleting saved places:', error);
        }
      }
    };

    const isDeleteAllDisabled = computed(() => {
      return savedPlaces.value.length === 0;
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
      isDeleteAllDisabled,
      visibleCards,  // Return visibleCards
      initialRender,  // Return initialRender
      navigateToGeneratedItinerary,
      toggleItinerary,
      toggleModal,
      isPlaceInItinerary,
      removePlace,
      filterPlaces,
      deleteAllPlaces,
      confirmDeleteAllPlaces,
      toggleDeletePopup
    };
  }
};
</script>

<style scoped>
/* General Page Styles */
.itinerary-page {
  font-family: 'Roboto', sans-serif;
  margin: 0;
  padding: 0;
}

.sticky-top {
  top: 0;
  position: sticky;
  z-index: 1020;
  background-color: black;
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
  font-family: 'Roboto', sans-serif;
  font-size: 1.5rem;
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

/* Card Styles */
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
  justify-content: space-between;
  height: 400px;
  padding: 10px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.destination-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}

.card-img-top {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.card-body {
  padding: 10px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

/* Button Styles */
.btn {
  background-color: black;
  color: white;
  border: none;
}

.btn:hover {
  background-color: #333;
  color: white;
}

.itinerary-button {
  width: 100%;
  padding: 10px;
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
  color: white;
}

/* Modal Styles */
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

.close-modal-btn:hover {
  background-color: #333;
  color: white;
}

/* Pop-up Styles */
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
}

.popup[style='background-color: #f44336;'] {
  background-color: #f44336;
}

/* Transitions */
.list-enter-active, .list-leave-active {
  transition: all 0.5s ease;
}

.list-enter, .list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.modal-enter-active, .modal-leave-active {
  transition: opacity 0.5s ease;
}

.modal-enter, .modal-leave-to {
  opacity: 0;
}

.popup-fade-enter-active, .popup-fade-leave-active {
  transition: opacity 0.5s ease;
}

.popup-fade-enter, .popup-fade-leave-to {
  opacity: 0;
}

.transition-wrapper {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  gap: 15px;
  padding: 20px;
}
</style>
