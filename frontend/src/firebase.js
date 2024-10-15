import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, FacebookAuthProvider } from "firebase/auth";
import { getFirestore, doc, setDoc } from "firebase/firestore"; // Keeping doc and setDoc to store user data

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

const db = getFirestore(app); // Firestore initialized

// Initialize Authentication and Providers
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();
const facebookProvider = new FacebookAuthProvider();

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
        this.$router.push('/');
    } catch (error) {
        console.error("Error storing user data:", error);
    }
}

// Export for use in other files
export { auth, googleProvider, facebookProvider, db, storeUserData };
