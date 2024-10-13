import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, FacebookAuthProvider } from "firebase/auth";

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

// Check if Firebase initialized successfully
console.log("Firebase app initialized:", app);

// Initialize Authentication and GoogleAuthProvider
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();
const facebookProvider = new FacebookAuthProvider();
// Export for use in other files
export { auth, googleProvider, facebookProvider };
