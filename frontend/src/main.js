import { createApp, reactive } from 'vue';
import App from './App.vue';
import router from './router';
import { Loader } from '@googlemaps/js-api-loader'; // Import Google Maps API Loader

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
    apiKey: 'AIzaSyDd5eMLnn0oB1z4JqV3QWgRhFWYJ1PFI0k', // Replace with your actual API key
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
    async loadItinerary(userId) {
        console.log(`Loading itinerary for user: ${userId}`);
        try {
            const snapshot = await db.collection('itineraries').doc(userId).get();
            if (snapshot.exists) {
                this.itinerary = snapshot.data().places;
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
            await updateDoc(doc(db, "users", userId), {
                'savedForItinerary.itinerary': arrayUnion(place)
            });
            console.log("Place added to itinerary");
        }
    },
    async removeFromItinerary(userId, placeId) {
        this.itinerary = this.itinerary.filter(place => place.place_id !== placeId);
        await updateDoc(doc(db, "users", userId), {
            'savedForItinerary.itinerary': arrayRemove({ place_id: placeId })
        });
        console.log("Place removed from itinerary");
    },
    async clearItinerary(userId) {
        this.itinerary = [];
        await updateDoc(doc(db, "users", userId), {
            'savedForItinerary.itinerary': []
        });
        console.log("Itinerary cleared");
    }
});

// Function to store user data
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
vueApp.provide('extractedLocationsState', extractedLocationsState);
vueApp.provide('apiPromise', apiPromise); // Provide apiPromise globally

// Use router, BootstrapVue3, and VCalendar
vueApp.use(router);
vueApp.use(BootstrapVue3);
vueApp.use(VCalendar);

// Mount the app
vueApp.mount('#app');

// Export Firebase auth and Firestore utilities
export { auth, db, storeUserData, googleProvider, facebookProvider };