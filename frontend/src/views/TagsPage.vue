<template>
    <div class="tags-page">
        <!-- Progress Bar -->
        <div class="progress-container">
            <div class="progress-bar" :style="{ width: progress + '%' }"></div>
            <p>{{ progressText }}</p>
        </div>

        <!-- Title and Subtitle -->
        <h2>Tell us what you're interested in</h2>
        <p>Select up to 10 tags. You can add up to 5 custom tags.</p>

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
                :disabled="newTag.length === 0 || customTags.length >= 5 || selectedTags.length >= 10">Add Tag</button>
        </div>

        <!-- Action Button -->
        <div class="actions">
            <button class="btn-secondary" @click="goBack">Back</button>
            <button class="btn-primary" @click="goToNextStep"
                :disabled="selectedTags.length === 0 || selectedTags.length > 10">Next Step</button>
        </div>

        <!-- Error message when tag limit is reached -->
        <p v-if="selectedTags.length >= 10" class="error">You can only select a maximum of 10 tags.</p>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import router from '@/router';
import { getFirestore, doc, getDoc } from 'firebase/firestore';  // Import Firebase Firestore
import { getAuth } from 'firebase/auth';  // Import Firebase Auth

// Firebase setup
const db = getFirestore();
const auth = getAuth();

// General tags (use more general ones)
const tags = ref([
    'Must-see Attractions', 'Great Food', 'Hidden Gems', 'Adventure Activities', 'Nature and Wildlife',
    'Cultural Heritage', 'Nightlife and Entertainment', 'Shopping', 'Beach Activities', 'Water Sports'
]);

const selectedTags = ref([]);  // Start empty
const customTags = ref([]);  // Custom tags will be added here
const newTag = ref('');  // For storing the new custom tag input

const allTags = ref([...tags.value]);  // Initialize with default tags
const progress = ref(75);  // Assuming it's the 3rd step of 4
const progressText = ref('Step 3 of 4: Select Tags');

const savedItinerary = ref([]);

// Fetch the saved itinerary from Firebase on component mount
onMounted(async () => {
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

// Toggle the selected state of a tag
const toggleTag = (tag) => {
    // Check if the tag is already selected
    if (selectedTags.value.includes(tag)) {
        // If selected, remove it
        selectedTags.value = selectedTags.value.filter(t => t !== tag);
    } else if (selectedTags.value.length < 10) {
        // If not selected and the limit is not reached, add the tag
        selectedTags.value.push(tag);
    }
};

const addCustomTag = () => {
    if (newTag.value.trim() !== '' && !customTags.value.includes(newTag.value) && selectedTags.value.length < 10) {
        // Add the new custom tag to both customTags and selectedTags
        customTags.value.push(newTag.value);
        selectedTags.value.push(newTag.value);
        allTags.value.push(newTag.value);  // Add the new custom tag to allTags for display

        newTag.value = '';  // Clear the input field
    }
};

const goBack = () => {
    router.back();
};

const goToNextStep = () => {
    // Extract the start, end, and tripType from the query params
    const { start, end, countryCode, tripType } = router.currentRoute.value.query;
    
    // Ensure start and end are Date objects before calling toISOString
    const startDate = new Date(start); // Convert to Date object
    const endDate = new Date(end);     // Convert to Date object   
    
    console.log('Passing information to generate itinerary page:');
    console.log('Selected Tags:', selectedTags.value);
    console.log('Itinerary:', savedItinerary.value);
    console.log('Start Date:', startDate);
    console.log('End Date:', endDate);
    console.log('Country Code:', countryCode);
    console.log('Trip Type:', tripType);
    
    // Navigate to the next step with the correct query parameters
    router.push({
        name: 'GenIti',
        query: {
            start: startDate.toISOString(),  // Convert Date object to ISO string
            end: endDate.toISOString(),      // Convert Date object to ISO string
            countryCode: countryCode,
            tripType: tripType,
            itinerary: JSON.stringify(savedItinerary.value),  // Pass itinerary from Firebase
            selectedTags: JSON.stringify(selectedTags.value)
        }
    });
};
</script>

<style scoped>
/* Progress bar styling */
.progress-container {
    margin: 20px 0;
    height: 25px;
    background-color: #f3f3f3;
    border-radius: 5px;
    overflow: hidden;
    position: relative;
    align-self: center;
}

.progress-bar {
    background-color: #4caf50;
    height: 100%;
    transition: width 0.4s;
}

/* Tags container */
.tags-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin: 20px 0;
}

button {
    padding: 10px 20px;
    background-color: #ddd;
    /* Default gray */
    border: none;
    border-radius: 20px;
    cursor: pointer;
    white-space: nowrap;
    transition: background-color 0.3s;
}

button.selected {
    background-color: #4caf50;
    /* Green when selected */
    color: white;
}

/* Custom tag section */
.add-custom-tag {
    margin: 20px 0;
    display: flex;
    gap: 10px;
}

.add-custom-tag input {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    flex-grow: 1;
}

/* Action buttons */
.actions {
    margin-top: 20px;
    text-align: center;
}

button:hover {
    background-color: #ccc;
}

/* Error message styling */
.error {
    color: red;
    font-weight: bold;
}
</style>