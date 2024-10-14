// main.js
import { createApp } from 'vue';
import App from './views/App.vue'; // Main App component
import router from './router'; // Router instance
import { initializeApp } from 'firebase/app'
import { getAuth, setPersistence, browserLocalPersistence } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';



// Create the Vue application

const firebaseConfig = {
  apiKey: "AIzaSyAAJFpBoEJzVfrj8Ix_YTZPc0QifkaMyKw",
  authDomain: "wander-wad.firebaseapp.com",
  projectId: "wander-wad",
  storageBucket: "wander-wad.appspot.com",
  messagingSenderId: "109364472671",
  appId: "1:109364472671:web:ff4324430b45ba7b58a4ea",
  measurementId: "G-TZHQN5ZWG4",
};

const fireapp = initializeApp(firebaseConfig);

const db = getFirestore(fireapp);

const auth = getAuth(fireapp);
// if (location.hostname === "localhost") {
//   connectAuthEmulator(auth, "http://localhost:9099");
// }
setPersistence(auth, browserLocalPersistence).catch((error) => {
  console.error("Error setting persistence:", error);
});

const app = createApp(App);

// Use the router
app.use(router);

// Mount the app
app.mount('#app');

export { auth, db };
