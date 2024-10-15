<template>
  <div class="homepage">
    <p class="searchBarTitle">Where would you like to wander?</p>
    
    <SearchBar @submit-link="handleLinkSubmit" />

    <!-- Displaying saved places -->
    <div v-if="savedPlaces.length > 0" class="saved-places">
      <h3>Saved Places</h3>
      <ul>
        <li v-for="place in savedPlaces" :key="place.name">
          <strong>{{ place.name }}</strong> - {{ place.location }}: {{ place.description }}
        </li>
      </ul>
    </div>

    <!-- Displaying generated itineraries -->
    <div v-if="generatedItineraries.length > 0" class="generated-itineraries">
      <h3>Generated Itineraries</h3>
      <ul>
        <li v-for="itinerary in generatedItineraries" :key="itinerary.destination">
          <strong>{{ itinerary.destination }}</strong> - {{ itinerary.duration }}:
          <ul>
            <li v-for="activity in itinerary.activities" :key="activity">{{ activity }}</li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import SearchBar from '@/components/SearchBar.vue';
import { doc, getDoc, updateDoc, arrayUnion } from "firebase/firestore";  // Import Firestore functions
import { db, auth } from "@/firebase";  // Import db and auth from your Firebase setup
import { onAuthStateChanged } from 'firebase/auth'; // To get the current logged-in user

export default {
  name: 'MainPage',
  components: {
    SearchBar, // Register the SearchBar component
  },
  data() {
    return {
      userId: null, // Store user ID
      savedPlaces: [], // Store saved places
      generatedItineraries: [], // Store generated itineraries
    };
  },
  mounted() {
    // Get the currently authenticated user and fetch their Firestore data
    onAuthStateChanged(auth, async (user) => {
      if (user) {
        this.userId = user.uid;
        console.log("User ID:", this.userId);
        await this.fetchUserData();

        // Optional: Add test data if it is a new user
        if (this.savedPlaces.length === 0 && this.generatedItineraries.length === 0) {
          await this.addTestData();
        }
      } else {
        console.log("No user is signed in.");
      }
    });
  },
  methods: {
    handleLinkSubmit(link) {
      console.log('Link submitted on Home Page:', link);
      // Handle the link submitted in this specific view
    },
    
    // Fetch the user data from Firestore
    async fetchUserData() {
      try {
        const userRef = doc(db, "users", this.userId);
        const userDoc = await getDoc(userRef);
        
        if (userDoc.exists()) {
          const userData = userDoc.data();
          this.savedPlaces = userData.savedPlaces || [];
          this.generatedItineraries = userData.generatedItineraries || [];
          console.log("User data fetched successfully:", userData);
        } else {
          console.log("No user data found.");
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    },

    // Add test data to Firestore
    async addTestData() {
      try {
        const userRef = doc(db, "users", this.userId);

        // Add a test saved place
        await updateDoc(userRef, {
          savedPlaces: arrayUnion({
            name: "Marina Bay Sands",
            location: "Singapore",
            description: "Iconic hotel with a rooftop infinity pool",
          }),
        });
        console.log("Test saved place added.");

        // Add a test generated itinerary
        await updateDoc(userRef, {
          generatedItineraries: arrayUnion({
            destination: "Japan",
            activities: ["Visit Tokyo Tower", "Explore Shibuya Crossing", "Eat Sushi"],
            duration: "5 days",
          }),
        });
        console.log("Test itinerary added.");
      } catch (error) {
        console.error("Error adding test data:", error);
      }
    },
  }
};
</script>


<style scoped>
.homepage {
  text-align: center;
  padding-top: 50px;
  padding: 5%;
}

.searchBarTitle {
  font-size: 3rem;
  margin-bottom: 20px;
  font-family: 'Cormorant Garamond', serif;
  font-weight: bold;
}

.saved-places, .generated-itineraries {
  margin-top: 40px;
}

.saved-places ul, .generated-itineraries ul {
  list-style-type: none;
  padding: 0;
}

.saved-places li, .generated-itineraries li {
  margin: 10px 0;
}
</style>
