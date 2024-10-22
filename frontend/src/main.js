import { createApp, reactive } from 'vue';
import App from './App.vue';
import router from './router';

// Bootstrap imports
import 'bootstrap/dist/css/bootstrap.min.css'; // Bootstrap CSS
import 'bootstrap/dist/js/bootstrap.bundle.js'; // Bootstrap JS (includes Popper.js)

// Firebase imports
import { initializeApp } from 'firebase/app';
import { getAuth, setPersistence, browserLocalPersistence, GoogleAuthProvider, FacebookAuthProvider } from 'firebase/auth';
import { getFirestore, doc, setDoc, getDoc, updateDoc, arrayUnion, arrayRemove } from 'firebase/firestore';

// BootstrapVue3 imports
import BootstrapVue3 from 'bootstrap-vue-3';
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'; // BootstrapVue3 CSS

// VCalendar imports

import VCalendar from 'v-calendar';
import 'v-calendar/style.css';


// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAAJFpBoEJzVfrj8Ix_YTZPc0QifkaMyKw",
  authDomain: "wander-wad.firebaseapp.com",
  projectId: "wander-wad",
  storageBucket: "wander-wad.appspot.com",
  messagingSenderId: "109364472671",
  appId: "1:109364472671:web:ff4324430b45ba7b58a4ea",
  measurementId: "G-TZHQN5ZWG4"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
console.log("Firebase app initialized:", app);

// Initialize Firestore and Auth
const db = getFirestore(app);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();
const facebookProvider = new FacebookAuthProvider();

// Set Firebase auth persistence
setPersistence(auth, browserLocalPersistence).catch((error) => {
    console.error("Error setting persistence:", error);
});

// Global state for saved places and itinerary (using Firebase)
const savedPlacesState = reactive({
    savedPlaces: [],

    async loadSavedPlaces(userId) {
      try {
          console.log("Loading saved places for user:", userId);
          const userDoc = await getDoc(doc(db, "users", userId));
          console.log("Firebase document data:", userDoc.data());
          // Process saved places...
      } catch (error) {
          console.error("Error loading saved places:", error);
      }
  },
  

    async addPlace(userId, place) {
        if (!this.savedPlaces.some(savedPlace => savedPlace.place_id === place.place_id)) {
            this.savedPlaces.push(place);
            await updateDoc(doc(db, "users", userId), {
                savedPlaces: arrayUnion(place)
            });
            console.log("Place added to saved places");
        }
    },

    async removePlace(userId, placeId) {
        this.savedPlaces = this.savedPlaces.filter(place => place.place_id !== placeId);
        await updateDoc(doc(db, "users", userId), {
            savedPlaces: arrayRemove({ place_id: placeId })
        });
        console.log("Place removed from saved places");
    }
});

const itineraryState = reactive({
    itinerary: [],

    async addToItinerary(userId, place) {
        try {
          if (!this.itinerary.some(item => item.place_id === place.place_id)) {
            this.itinerary.push(place);
      
            // Update Firebase under "savedForItinerary"
            await updateDoc(doc(db, "users", userId), {
              'savedForItinerary.itinerary': arrayUnion(place)  // Make sure 'place_id' exists in the place object
            });
            console.log("Place added to itinerary");
          } else {
            console.log("Place already exists in the itinerary.");
          }
        } catch (error) {
          console.error("Error adding place to itinerary:", error);
        }
      },
  
    // Add a place to the "savedForItinerary.itinerary" field
    async loadItinerary(userId) {
        try {
          const userDoc = await getDoc(doc(db, "users", userId));
          if (userDoc.exists()) {
            console.log("Fetched data from Firebase:", userDoc.data()); // ADD THIS LINE
            const savedForItinerary = userDoc.data().savedForItinerary;
            this.itinerary = savedForItinerary ? savedForItinerary.itinerary || [] : [];
          } else {
            console.log("No itinerary found.");
            this.itinerary = []; // Ensure it's reset if nothing is found
          }
        } catch (error) {
          console.error("Error loading itinerary:", error);
        }
      },
  
    // Remove a place from the "savedForItinerary.itinerary" field
    async removeFromItinerary(userId, placeId) {
        try {
          this.itinerary = this.itinerary.filter(place => place.place_id !== placeId);
      
          // Update Firebase under "savedForItinerary"
          await updateDoc(doc(db, "users", userId), {
            'savedForItinerary.itinerary': arrayRemove({ place_id: placeId })  // Make sure this matches the exact object
          });
      
          console.log("Place removed from itinerary");
        } catch (error) {
          console.error("Error removing place from itinerary:", error);
        }
      },
  
    // Clear the itinerary (resets both local state and Firebase)
    async clearItinerary(userId) {
      try {
        this.itinerary = [];
  
        // Update Firebase to clear the itinerary
        await updateDoc(doc(db, "users", userId), {
          'savedForItinerary.itinerary': []
        });
  
        console.log("Itinerary cleared");
      } catch (error) {
        console.error("Error clearing itinerary:", error);
      }
    }
  });
  

// Function to store user data (called when a new user is created or signs in)
async function storeUserData(userId, email) {
    try {
        const userRef = doc(db, "users", userId);
        await setDoc(userRef, {
            email: email,
            savedPlaces: [],
            generatedItineraries: []
        }, { merge: true });
        console.log("User data stored successfully");
    } catch (error) {
        console.error("Error storing user data:", error);
    }
}

// Create Vue app
const vueApp = createApp(App);

const extractedLocationsState = reactive({
    locationInfo: null,
    relatedPlaces: [],
    // Add any other shared state properties
    setLocationInfo(info) {
        this.locationInfo = info;
      },
    
      setRelatedPlaces(places) {
        this.relatedPlaces = places;
      }
  });

// Provide global states to the app
vueApp.provide('savedPlacesState', savedPlacesState);
vueApp.provide('itineraryState', itineraryState);
vueApp.provide('extractedLocationsState', extractedLocationsState);

// Use router, BootstrapVue, and Google Login
vueApp.use(router);
vueApp.use(BootstrapVue3);
vueApp.use(VCalendar, {})

// Mount the app
vueApp.mount('#app');

// Export Firebase auth and Firestore utilities
export { auth, db, storeUserData, googleProvider, facebookProvider };
