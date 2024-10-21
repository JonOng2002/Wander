<template>
    <div class="tags-page">
        <!-- Progress Bar -->
        <div class="progress-container">
            <div class="progress-bar" :style="{ width: progress + '%' }"></div>
            <p>{{ progressText }}</p>
        </div>

        <!-- Title and Subtitle -->
        <h2>Tell us what you're interested in</h2>
        <p>Select all that apply.</p>

        <!-- Tags List -->
        <div class="tags-container">
            <button v-for="tag in tags" :key="tag" :class="{ 'selected': selectedTags.includes(tag) }"
                @click="toggleTag(tag)">
                {{ tag }}
            </button>
        </div>

        <!-- Action Button -->
        <div class="actions">
            <button class="btn-secondary" @click="goBack">Back</button>
            <button class="btn-primary" @click="goToNextStep">Next Step</button>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import router from '@/router';

// Static tags for now, can be dynamic later
const tags = ref([
    'Must-see Attractions', 'Great Food', 'Hidden Gems', 'Luau Extravaganza',
    'Ocean Adventures in Oahu', 'Surfing Lessons in Waikiki', 'Hawaiian Cuisine',
    'Surfing', 'Hawaiian Culture and History', 'Nature and Wildlife',
    'Nightlife and Entertainment', 'Luxury Shopping', '+ Add Interest'
]);

// State for selected tags
const selectedTags = ref([]);

// Progress bar state
const progress = ref(75);  // Assuming it's the 3rd step of 4
const progressText = ref('Step 3 of 4: Select Tags');

// Toggle tag selection
const toggleTag = (tag) => {
    if (selectedTags.value.includes(tag)) {
        selectedTags.value = selectedTags.value.filter(t => t !== tag);
    } else {
        selectedTags.value.push(tag);
    }
};

// Go back to previous step
const goBack = () => {
    router.back();
};

// Proceed to next step (send tags to GenItineraryTest.vue)
const goToNextStep = () => {
  const { start, end, tripType, itinerary } = router.currentRoute.value.query; // Receive previous data
  if (selectedTags.value.length === 0) {
    console.log('No tags selected.');
    return;
  }

  router.push({
  name: 'GenItiTest',
  query: {
    start: new Date(start).toISOString(),  // Use ISO string
    end: new Date(end).toISOString(),
    tripType,
    itinerary,
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
    border: none;
    border-radius: 20px;
    cursor: pointer;
    white-space: nowrap;
}

button.selected {
    background-color: #4caf50;
    color: white;
}

.actions {
    margin-top: 20px;
    text-align: center;
}

button:hover {
    background-color: #ccc;
}
</style>