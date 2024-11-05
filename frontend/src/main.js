// src/main.js

import { createApp, reactive } from 'vue';
import App from './App.vue';
import router from './router';
import { Loader } from '@googlemaps/js-api-loader'; // Import Google Maps API Loader
import { autoAnimatePlugin } from '@formkit/auto-animate/vue'

// FormKit imports
import { plugin, defaultConfig } from '@formkit/vue';

//motion pluggin imports
import { MotionPlugin } from '@vueuse/motion'

// Bootstrap imports
import 'bootstrap/dist/css/bootstrap.min.css'; // Bootstrap CSS
import 'bootstrap/dist/js/bootstrap.bundle.js'; // Bootstrap JS (includes Popper.js)

// Firebase imports
import { initializeApp } from 'firebase/app';
import { 
  getAuth, 
  setPersistence, 
  browserLocalPersistence, 
  GoogleAuthProvider, 
  FacebookAuthProvider 
} from 'firebase/auth';
import { 
  getFirestore, 
  doc, 
  getDoc, 
  setDoc, 
  updateDoc, 
  arrayUnion, 
  arrayRemove 
} from 'firebase/firestore';

// BootstrapVue3 imports
import BootstrapVue3 from 'bootstrap-vue-3';
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'; // BootstrapVue3 CSS

// VCalendar imports
import VCalendar from 'v-calendar';
import 'v-calendar/style.css';

// Firebase configuration
const firebaseConfig = {
    apiKey: process.env.VUE_APP_FIREBASE_API_KEY,
    authDomain: process.env.VUE_APP_FIREBASE_AUTH_DOMAIN,
    projectId: process.env.VUE_APP_FIREBASE_PROJECT_ID,
    storageBucket: process.env.VUE_APP_FIREBASE_STORAGE_BUCKET,
    messagingSenderId: process.env.VUE_APP_FIREBASE_MESSAGING_SENDER_ID,
    appId: process.env.VUE_APP_FIREBASE_APP_ID,
    measurementId: process.env.VUE_APP_MEASUREMENT_ID
  };

// Initialize Firebase
const firebaseApp = initializeApp(firebaseConfig);
console.log("Firebase app initialized:", firebaseApp);

// Initialize Firestore and Auth
const db = getFirestore(firebaseApp);
const auth = getAuth(firebaseApp);
const googleProvider = new GoogleAuthProvider();
const facebookProvider = new FacebookAuthProvider();

// Set Firebase auth persistence
setPersistence(auth, browserLocalPersistence).catch((error) => {
  console.error("Error setting persistence:", error);
});

// Initialize Google Maps API using Loader
const loader = new Loader({
    apiKey: process.env.VUE_APP_GOOGLE_API_KEY, // Replace with your actual API key
    version: 'weekly',
    libraries: ['places'],
});

// Load the Google Maps API and store the promise
const apiPromise = loader.load();

// Global state for saved places and itinerary (using Firebase)
const savedPlacesState = reactive({
  savedPlaces: [],
  async loadSavedPlaces(userId) {
    try {
      console.log("Loading saved places for user:", userId);
      const userDoc = await getDoc(doc(db, "users", userId));
      console.log("Firebase document data:", userDoc.data());
      if (userDoc.exists()) {
        const loadedPlaces = userDoc.data().savedPlaces || [];

        // Remove duplicates by creating a Set for unique place IDs
        const uniquePlaces = Array.from(
          new Map(
            loadedPlaces.map((place) => [place.place_id.toLowerCase(), place])
          ).values()
        );

        this.savedPlaces = uniquePlaces;
      } else {
        console.log("No saved places found for this user.");
        this.savedPlaces = [];
      }
    } catch (error) {
      console.error("Error loading saved places:", error);
      this.savedPlaces = [];
    }
  },
  async addPlace(userId, place) {
    // Case-insensitive duplicate check
    const placeExists = this.savedPlaces.some(
      (savedPlace) => savedPlace.place_id.toLowerCase() === place.place_id.toLowerCase()
    );

    if (placeExists) {
      console.log("Place already saved:", place.name);
      return false; // Indicate that the place was not added because it already exists
    }

    this.savedPlaces.push(place); // Add the new place locally

    try {
      // Fetch the current user's saved places
      const userRef = doc(db, "users", userId);
      const userDoc = await getDoc(userRef);
      let updatedSavedPlaces = [];

      if (userDoc.exists()) {
        updatedSavedPlaces = userDoc.data().savedPlaces || [];
      }

      // Add the new place
      updatedSavedPlaces.push(place);

      // Update Firestore with the new list of saved places
      await setDoc(userRef, { savedPlaces: updatedSavedPlaces }, { merge: true });

      console.log("Place added to saved places");
      return true; // Indicate successful addition
    } catch (error) {
      console.error("Error adding place to saved places:", error);
      // Optionally, remove the place from the local state if Firestore update fails
      this.savedPlaces = this.savedPlaces.filter(
        (savedPlace) => savedPlace.place_id.toLowerCase() !== place.place_id.toLowerCase()
      );
      return false; // Indicate failure
    }
  },
  async removePlace(userId, placeId) {
    this.savedPlaces = this.savedPlaces.filter(
      (place) => place.place_id.toLowerCase() !== placeId.toLowerCase()
    );
    try {
      await updateDoc(doc(db, "users", userId), {
        savedPlaces: arrayRemove({ place_id: placeId })
      });
      console.log("Place removed from saved places");
    } catch (error) {
      console.error("Error removing place from saved places:", error);
    }
  },
  async clearSavedPlaces() {
    this.savedPlaces = [];
  }
});

const itineraryState = reactive({
  itinerary: [],
  async loadItinerary(userId) {
    console.log(`Loading itinerary for user: ${userId}`);
    try {
      const snapshot = await getDoc(doc(db, 'itineraries', userId));
      if (snapshot.exists()) {
        this.itinerary = snapshot.data().places || [];
        console.log('Itinerary loaded:', this.itinerary);
      } else {
        console.log('No itinerary found for this user.');
        this.itinerary = [];
      }
    } catch (error) {
      console.error('Error loading itinerary:', error);
    }
  },
  async addToItinerary(userId, place) {
    if (!this.itinerary.some(item => item.place_id === place.place_id)) {
      this.itinerary.push(place);
      try {
        await updateDoc(doc(db, "users", userId), {
          'savedForItinerary.itinerary': arrayUnion(place)
        });
        console.log("Place added to itinerary");
      } catch (error) {
        console.error("Error adding place to itinerary:", error);
      }
    }
  },
  async removeFromItinerary(userId, placeId) {
    this.itinerary = this.itinerary.filter(place => place.place_id !== placeId);
    try {
      await updateDoc(doc(db, "users", userId), {
        'savedForItinerary.itinerary': arrayRemove({ place_id: placeId })
      });
      console.log("Place removed from itinerary");
    } catch (error) {
      console.error("Error removing place from itinerary:", error);
    }
  },
  async clearItinerary(userId) {
    this.itinerary = [];
    try {
      await updateDoc(doc(db, "users", userId), {
        'savedForItinerary.itinerary': []
      });
      console.log("Itinerary cleared");
    } catch (error) {
      console.error("Error clearing itinerary:", error);
    }
  }
});

const savedItineraryState = reactive({
  toSaveItinerary: [],

  async loadSavedItinerary(userId) {
    try {
      const userDoc = await getDoc(doc(db, "users", userId));
      if (userDoc.exists()) {
        this.toSaveItinerary = userDoc.data().savedItineraries || [];
        console.log("Saved itineraries loaded successfully");
      } else {
        console.log("No itineraries found.");
        this.toSaveItinerary = [];
      }
    } catch (error) {
      console.error("Error loading saved itineraries:", error);
    }
  },

  async addToSavedItinerary(userId, place) {
    if (!this.toSaveItinerary.some(savedPlace => savedPlace.place_id === place.place_id)) {
      this.toSaveItinerary.push(place);
      try {
        await updateDoc(doc(db, "users", userId), {
          savedItineraries: arrayUnion(place)
        });
        console.log("Place added to saved itinerary");
      } catch (error) {
        console.error("Error adding place to saved itinerary:", error);
      }
    }
  },

  async removeFromSavedItinerary(userId, placeId) {
    this.toSaveItinerary = this.toSaveItinerary.filter(place => place.place_id !== placeId);
    try {
      await updateDoc(doc(db, "users", userId), {
        savedItineraries: arrayRemove({ place_id: placeId })
      });
      console.log("Place removed from saved itinerary");
    } catch (error) {
      console.error("Error removing place from saved itinerary:", error);
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
      generatedItineraries: [],
      savedItineraries: []
    }, { merge: true });
    console.log("User data stored successfully");
  } catch (error) {
    console.error("Error storing user data:", error);
  }
}

// Create Vue app
const vueApp = createApp(App);

// Global state for extracted locations
const extractedLocationsState = reactive({
  locationInfo: null,
  relatedPlaces: [],
  setLocationInfo(info) {
    this.locationInfo = info;
  },
  setRelatedPlaces(places) {
    this.relatedPlaces = places;
  }
});

// Provide global states and Google Maps API promise to the app
vueApp.provide('savedPlacesState', savedPlacesState);
vueApp.provide('itineraryState', itineraryState);
vueApp.provide('savedItineraryState', savedItineraryState);
vueApp.provide('extractedLocationsState', extractedLocationsState);
vueApp.provide('apiPromise', apiPromise); // Provide apiPromise globally

// Use plugins
vueApp.use(router);
vueApp.use(BootstrapVue3);
vueApp.use(VCalendar);
vueApp.use(plugin, defaultConfig); // FormKit integration
vueApp.use(MotionPlugin);
console.log("MotionPlugin registered");


vueApp.use(autoAnimatePlugin);

// Mount the app
vueApp.mount('#app');

// Export Firebase auth and Firestore utilities
export { auth, db, storeUserData, googleProvider, facebookProvider };
