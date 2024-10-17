<template>
  <!-- This Page is not styled yet, it fetches the saved places from user's firestore-->
  <div>
    <h2>Your Saved Places</h2>

    <div v-if="loading">Loading saved places...</div>
    <div v-else-if="savedPlaces.length === 0">You have no saved places yet.</div>
    <div v-else>
      <ul>
        <li v-for="place in savedPlaces" :key="place.id">
          <strong>{{ place.placeName }}</strong>
          <p>Summary: {{ place.summary || 'No summary available' }}</p>
          <p>Country: {{ place.country }}</p>
          <p>City: {{ place.city }}</p>
          <p>Latitude: {{ place.coordinates.latitude }}</p>
          <p>Longitude: {{ place.coordinates.longitude }}</p>
          <p>Activities: {{ place.activities?.join(', ') || 'No activities available' }}</p>
          <p>
          <img 
            :src="place.placePng" 
            @error="handleImageError" 
            width="300px" 
          />
          </p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getFirestore, collection, getDocs } from 'firebase/firestore';
import { getAuth, onAuthStateChanged } from 'firebase/auth';

// State management
const savedPlaces = ref([]);
const loading = ref(true);

// Initialize Firestore
const db = getFirestore();

onMounted(() => {
  const auth = getAuth();

  // Check authentication state
  onAuthStateChanged(auth, async (user) => {
    if (user) {
      const userId = user.uid;  // Get the user's ID

      try {
        const querySnapshot = await getDocs(collection(db, 'savedPlaces'));

        // Filter saved places based on userId
        savedPlaces.value = querySnapshot.docs
          .filter(doc => doc.data().userId === userId)
          .map(doc => ({
            id: doc.id,  // Get document ID
            ...doc.data(),  // Merge the rest of the data
          }));

      } catch (error) {
        console.error("Error fetching saved places:", error);
      } finally {
        loading.value = false;  // Stop the loading state
      }
    } else {
      console.error("User not logged in");
      loading.value = false;
    }
  });
});
const handleImageError = (event) => {
  event.target.src = 'https://i.postimg.cc/8zLP2XNf/Image-16-10-24-at-2-27-PM.jpg'; // Set the src to the alternative image URL
};

</script>

<style scoped>
/* Add any relevant styles */
</style>