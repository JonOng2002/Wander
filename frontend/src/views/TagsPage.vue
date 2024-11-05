<template>
  <div class="progress-container">
    <div class="progress-bar" :style="{ width: progress + '%' }"></div>
  </div>
  <div class="tags-page-layout">
    <!-- Centered Title -->
    <div class="title-wrapper">
      <a class="navbar-brand" href="#">
        <h1 id="title" class="h1">wander.</h1>
      </a>
    </div>

    <div class="content-wrapper">
      <!-- Left Image Card Section -->
      <div class="image-card">
        <img src="@/assets/tagsPage.jpg" alt="Travel Background" class="image-card-content" />
        <div class="image-card-overlay">
          <h1>Customise Your Perfect Getaway.</h1>
        </div>
      </div>

      <!-- Right Form Section -->
      <div class="form-section">
        <!-- Header Text -->
        <h2 class="form-header">Tell us what you're interested in</h2>
        <p class="form-subtext">Select up to 10 tags. You can add up to 5 custom tags.</p>

        <!-- Tags List -->
        <div class="tags-container">
          <button v-for="tag in allTags" :key="tag" :class="{ 'selected': selectedTags.includes(tag) }"
            @click="toggleTag(tag)">
            {{ tag }}
          </button>
        </div>

        <!-- Add Custom Tag -->
        <div class="add-custom-tag">
          <input v-model="newTag" type="text" placeholder="Add custom tag"
            :disabled="customTags.length >= 5 || selectedTags.length >= 10" @keyup.enter="addCustomTag" />
          <button @click="addCustomTag"
            :disabled="newTag.length === 0 || customTags.length >= 5 || selectedTags.length >= 10">
            Add Tag
          </button>
        </div>

        <!-- Action Buttons -->
        <div class="action-buttons">
          <button class="btn-back" @click="goBack">←</button>
          <button class="btn-primary" @click="goToNextStep"
            :disabled="selectedTags.length === 0 || selectedTags.length > 10">
            Generate Itinerary
          </button>
        </div>

        <!-- Error Message -->
        <p v-if="selectedTags.length >= 10" class="error">You can only select a maximum of 10 tags.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import router from '@/router';
import { getFirestore, doc, getDoc } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';

const db = getFirestore();
const auth = getAuth();

const tags = ref([
  'Must-see Attractions', 'Great Food', 'Hidden Gems', 'Adventure Activities', 'Nature and Wildlife',
  'Cultural Heritage', 'Nightlife and Entertainment', 'Shopping', 'Beach Activities', 'Water Sports'
]);

const selectedTags = ref([]);
const customTags = ref([]);
const newTag = ref('');

const allTags = ref([...tags.value]);
const progress = ref(75);

const savedItinerary = ref([]);

onMounted(async () => {
  const { start, end, countryCode, tripType } = router.currentRoute.value.query;
  console.log("Received data in TagsPage:");
  console.log("Start Date:", start);
  console.log("End Date:", end);
  console.log("Country Code:", countryCode);
  console.log("Trip Type:", tripType);

  const user = auth.currentUser;
  if (user) {
    const userDocRef = doc(db, "users", user.uid);
    const userDoc = await getDoc(userDocRef);
    if (userDoc.exists()) {
      savedItinerary.value = userDoc.data().generatedItineraries || [];
      console.log('Itinerary fetched from Firebase:', savedItinerary.value);
    } else {
      console.error("No itinerary found in Firebase.");
    }
  } else {
    console.error("User not authenticated.");
  }
});

const toggleTag = (tag) => {
  if (selectedTags.value.includes(tag)) {
    selectedTags.value = selectedTags.value.filter(t => t !== tag);
  } else if (selectedTags.value.length < 10) {
    selectedTags.value.push(tag);
  }
};

const addCustomTag = () => {
  if (newTag.value.trim() !== '' && !customTags.value.includes(newTag.value) && selectedTags.value.length < 10) {
    customTags.value.push(newTag.value);
    selectedTags.value.push(newTag.value);
    allTags.value.push(newTag.value);
    newTag.value = '';
  }
};

const goBack = () => {
  router.back();
};

const goToNextStep = () => {
  const { start, end, countryCode, tripType } = router.currentRoute.value.query;

  console.log("Sending data to GeneratedItinerary:");
  console.log("Selected Tags:", selectedTags.value);
  console.log("Itinerary:", savedItinerary.value);
  console.log("Start Date:", start);
  console.log("End Date:", end);
  console.log("Country Code:", countryCode);
  console.log("Trip Type:", tripType);

  router.push({
    name: 'GeneratedItinerary',
    query: {
      start,
      end,
      countryCode,
      tripType,
      itinerary: JSON.stringify(savedItinerary.value),
      selectedTags: JSON.stringify(selectedTags.value),
    },
  });
};
</script>

<style scoped>
/* Progress Bar */
.progress-container {
  width: 100%;
  height: 10px;
  overflow: hidden;
  margin-top: 10px;
}

.progress-bar {
  background-color: #2a5ead;
  height: 100%;
  transition: width 0.4s ease;
}

/* Page Layout */
.tags-page-layout {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
}

/* Centered Title */
.title-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

#title {
  font-family: "Lobster Two", cursive;
  font-size: 2.5vw;
  color: #2a5ead;
}

/* Content Wrapper */
.content-wrapper {
  display: flex;
  width: 100%;
  max-width: 1600px;
  gap: 2rem;
  height: 100%;
  align-items: stretch;
}

/* Left Image Card */
.image-card {
  flex: 1 1 50%;
  background-color: #fff;
  border-radius: 1rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 80vh;
}

.image-card-content {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-card-overlay {
  position: absolute;
  top: 20px;
  left: 30px;
  color: white;
  padding: 1rem;
  border-radius: 1rem;
  display: flex;
  flex-direction: column;
  max-width: 100%;
  
}

.image-card-overlay h1 {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  backdrop-filter: blur(2px); /* Applies the blur effect */
}

/* Form Section */
.form-section {
  flex: 1 1 50%;
  padding: 1rem 2rem 1rem 10rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;

}

.form-header {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #333;
}

.form-subtext {
  font-size: 0.9rem;
  margin-bottom: 1rem;
  color: #666;
}

/* Tags Container */
.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 20px 0;
}

button {
  padding: 10px 20px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button.selected {
  background: linear-gradient(90deg, #44c7f4, #3dd598);;
  color: white;
}

/* Custom Tag Section */
.add-custom-tag {
  display: flex;
  gap: 10px;
  margin-top: 1rem;
  background-color: transparent;
}

.add-custom-tag input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  flex-grow: 1;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin-top: 2rem;
}

.btn-back {
  width: 40px;
  height: 40px;
  border: 2px solid #ccc;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #333;
  font-size: 1.2rem;
  background-color: transparent;
}

.btn-primary {
  background: linear-gradient(90deg, #4a90e2, #8e44ad);
  color: white;
  padding: 0.5rem 2rem;
  border-radius: 25px;
  font-weight: bold;
  cursor: pointer;
}


/* <=================== breakpoints and media =======================>*/
/* Base styles (1200px and above) remain as is */

/* Base styles (1200px and above) remain as is */

/* XL to LG (1200px to 990px) */
@media (max-width: 1199px) and (min-width: 768px) {
  .content-wrapper {
    display: flex;
    align-items: center; /* Centers the contents vertically */
    justify-content: center; /* Centers the contents horizontally */
    gap: 2rem;
    max-height: 90vh; /* Limits the overall height of content-wrapper */
  }

  .form-section {
    height: auto; /* Allow form-section to expand naturally */
    padding: 1rem 1.5rem; /* Reduces excessive padding */
    margin: 0 auto; /* Ensures horizontal centering */
    box-sizing: border-box;
  }
}

/* LG to MD (990px to 768px) */
/* No changes required as per instructions */

/* Below MD (less than 768px) */
@media (max-width: 767px) {
  .content-wrapper {
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .image-card {

    width: 100%; /* Makes image-card take full width */
    max-width: 500px; /* Optional: restricts width to avoid excessive stretching */
    height: 40vh; /* Adjust height to fit smaller screens */
    max-height: 400px; /* Limit height to prevent excessive scrolling */
    margin: 0 auto; /* Centers the image card */
  }
  
  .form-section {
    width: 100%; /* Makes form-section take full width */
    max-width: 500px; /* Optional: restricts width to avoid excessive stretching */
    padding: 1rem; /* Adjust padding for better spacing on small screens */
    margin: 0 auto; /* Centers the form section */
    height: auto; /* Allow natural expansion */
  }
}
@media (min-width: 768px) and (max-width: 991px) {
  .content-wrapper {
    flex-direction: column;
  }
  .form-section {
    padding: 1rem 2rem;
    text-align: center;
    align-items: center;
  }
  .btn-primary{
    background: linear-gradient(90deg, #4a90e2, #8e44ad); /* Gradient colors */
  color: white;
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 25px; /* Rounded edges */
  font-weight: bold;
  cursor: pointer;
  font-size: 1rem;
  transition: transform 0.2s, box-shadow 0.2s;
  margin-left: 1rem; /* Space between buttons */
  height: 50px;
  flex-grow: 1; /* Allow the button to expand to available space */
  max-width: 400px;
  }
  .image-card-content{
    height: 80vh;
  }
}

</style>