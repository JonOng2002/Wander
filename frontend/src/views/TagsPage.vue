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
import { ref, toRaw } from 'vue';
import router from '@/router';

// General tags (use more general ones)
const tags = ref([
    'Must-see Attractions', 'Great Food', 'Hidden Gems', 'Adventure Activities', 'Nature and Wildlife',
    'Cultural Heritage', 'Nightlife and Entertainment', 'Shopping', 'Beach Activities', 'Water Sports'
]);

// State for selected and custom tags
const selectedTags = ref([]);  // Start empty
const customTags = ref([]);  // Custom tags will be added here
const newTag = ref('');  // For storing the new custom tag input

// Combine built-in and custom tags for display
const allTags = ref([...tags.value]);  // Initialize with default tags

// Progress bar state
const progress = ref(75);  // Assuming it's the 3rd step of 4
const progressText = ref('Step 3 of 4: Select Tags');

// Toggle tag selection (built-in and custom tags)
const toggleTag = (tag) => {
    if (selectedTags.value.includes(tag)) {
        // If the tag is already selected, deselect it
        selectedTags.value = selectedTags.value.filter(t => t !== tag);
        console.log('Tag deselected:', tag);
    } else if (selectedTags.value.length < 10) {
        // Select the tag if not already selected and below the limit of 10
        selectedTags.value.push(tag);
        console.log('Tag selected:', tag);
    }
    // Log the current selection
    console.log('Current Selected Tags:', selectedTags.value);
};

// Add custom tag with a maximum limit of 5 custom tags
const addCustomTag = () => {
    if (newTag.value.trim() !== '' && !customTags.value.includes(newTag.value) && selectedTags.value.length < 10) {
        // Add the new tag to both customTags and selectedTags
        customTags.value.push(newTag.value);
        selectedTags.value.push(newTag.value);
        allTags.value.push(newTag.value);  // Add the new custom tag to allTags for display

        // Log the action to check if tags are added
        console.log('New Custom Tag Added:', newTag.value);
        console.log('Updated Selected Tags:', selectedTags.value);

        newTag.value = '';  // Clear input field after adding
    }
};

// Go back to previous step
const goBack = () => {
    router.back();
};

// Proceed to the next step (send selected tags and other data)
const goToNextStep = () => {
    const { start, end, tripType, itinerary } = router.currentRoute.value.query; // Receive previous data

    // Convert itinerary to a plain JavaScript object to avoid circular references
    const rawItinerary = toRaw(itinerary);

    // Log to check if selected tags are sent correctly
    console.log('Proceeding with Selected Tags:', selectedTags.value);

    router.push({
        name: 'GenItiTest',
        query: {
            start: new Date(start).toISOString(),
            end: new Date(end).toISOString(),
            tripType,
            itinerary: JSON.stringify(rawItinerary),  // Convert to raw JavaScript object
            selectedTags: JSON.stringify(toRaw(selectedTags.value))  // Pass plain array, not reactive object
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