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

// Google Login integration
import { vue3GoogleLogin } from 'vue3-google-login';

// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyBVl2PcKsshkWYITyO3jFBVkKNLObqRIX4",
    authDomain: "wad2-proj-g8t9.firebaseapp.com",
    projectId: "wad2-proj-g8t9",
    storageBucket: "wad2-proj-g8t9.appspot.com",
    messagingSenderId: "492171564263",
    appId: "1:492171564263:web:dd89e494ad078782fe3e42",
    measurementId: "G-63VKFQ7B15"
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

// Global state for saved places and generated itinerary (using Firebase)
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
        const userDoc = await getDoc(doc(db, "users", userId));
        if (userDoc.exists()) {
            this.itinerary = userDoc.data().generatedItineraries || [];
        } else {
            console.log("No itineraries found.");
        }
    },

    async addToItinerary(userId, place) {
        this.itinerary.push(place);
        await updateDoc(doc(db, "users", userId), {
            generatedItineraries: arrayUnion(place)
        });
        console.log("Place added to itinerary");
    },

    async removeFromItinerary(userId, placeId) {
        this.itinerary = this.itinerary.filter(place => place.place_id !== placeId);
        await updateDoc(doc(db, "users", userId), {
            generatedItineraries: arrayRemove({ place_id: placeId })
        });
        console.log("Place removed from itinerary");
    }
});

const savedItineraryState = reactive({
    toSaveitinerary: [],

    async loadSavedItinerary(userId) {
        const userDoc = await getDoc(doc(db, "users", userId));
        if (userDoc.exists()) {
            this.toSaveitinerary = userDoc.data().savedItineraries || [];
            console.log("Saved itineraries loaded successfully");
        } else {
            console.log("No itineraries found.");
        }
    },

    async addToSavedItinerary(userId, place) {
        this.toSaveitinerary.push(place);
        await updateDoc(doc(db, "users", userId), {
            savedItineraries: arrayUnion(place)
        });
        console.log("Place added to itinerary");
    },

    async removeFromSavedItinerary(userId, placeId) {
        this.toSaveitinerary = this.toSaveitinerary.filter(place => place.place_id !== placeId);
        await updateDoc(doc(db, "users", userId), {
            savedItineraries: arrayRemove({ place_id: placeId })
        });
        console.log("Place removed from itinerary");
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
vueApp.provide('savedItineraryState', savedItineraryState);
vueApp.provide('extractedLocationsState', extractedLocationsState);

// Use router, BootstrapVue, and Google Login
vueApp.use(router);
vueApp.use(BootstrapVue3);
vueApp.use(vue3GoogleLogin, {
    clientId: '534126756340-2vokn8in9452u0m1uretrg6n1it4cgni.apps.googleusercontent.com'
});

// Mount the app
vueApp.mount('#app');

// Export Firebase auth and Firestore utilities
export { auth, db, storeUserData, googleProvider, facebookProvider };
