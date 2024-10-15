import { createApp } from 'vue';
import App from './App.vue'; // Main App component
import router from './router'; // Router instance

// Firebase imports
import { initializeApp } from "firebase/app";
import { getAuth, setPersistence, browserLocalPersistence, GoogleAuthProvider, FacebookAuthProvider } from "firebase/auth";
import { getFirestore, doc, setDoc } from "firebase/firestore"; // Import necessary Firestore functions

// Bootstrap and BootstrapVue imports
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS
import 'bootstrap/dist/js/bootstrap.bundle.js'; // Import Bootstrap JS (includes Popper.js)
import BootstrapVue3 from 'bootstrap-vue-3';
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'; // Correct import for BootstrapVue3 CSS

// Google Login integration
import { vue3GoogleLogin } from 'vue3-google-login';

// Firebase configuration - replace with your actual configuration
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

// Initialize Firestore
const db = getFirestore(app); // Firestore initialized

// Initialize Authentication
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();
const facebookProvider = new FacebookAuthProvider();

// Set Firebase auth persistence
setPersistence(auth, browserLocalPersistence).catch((error) => {
    console.error("Error setting persistence:", error);
});

// Function to store user data in Firestore
async function storeUserData(userId, email) {
    try {
        const userRef = doc(db, "users", userId); // Get user document reference
        await setDoc(userRef, {
            email: email,
            savedPlaces: [],
            generatedItineraries: []
        }, { merge: true }); // Merge data to avoid overwriting existing fields
        console.log("User data stored successfully");
    } catch (error) {
        console.error("Error storing user data:", error);
    }
}

// Create the Vue application
const vueApp = createApp(App);

// Use router, BootstrapVue, and Google Login
vueApp.use(router); // Use the router in the app
vueApp.use(BootstrapVue3); // Use BootstrapVue3
vueApp.use(vue3GoogleLogin, {
    clientId: 'YOUR_GOOGLE_CLIENT_ID' // Make sure to replace this with your actual Google client ID
});

// Mount the app
vueApp.mount('#app');

// Export Firebase authentication and database for use in other parts of the app
export { auth, db, storeUserData, googleProvider, facebookProvider };