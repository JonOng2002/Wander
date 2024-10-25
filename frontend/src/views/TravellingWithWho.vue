<template>
    <div class="travel-type-page">
      <!-- Progress Bar -->
      <div class="progress-container">
        <div class="progress-bar" :style="{ width: progress + '%' }"></div>
        <p>{{ progressText }}</p>
      </div>
  
      <h2>What kind of trip are you planning?</h2>
      <p>Select one.</p>
  
      <!-- Trip Type Options -->
      <div class="trip-options">
        <button
          v-for="type in tripTypes"
          :key="type.id"
          :class="{'selected': selectedTripType === type.id}"
          @click="selectTripType(type.id)"
        >
          {{ type.label }}
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
  
  // Progress bar state
  const progress = ref(50);  // Update progress for this step
  const progressText = ref('Step 2 of 4: Select Trip Type');
  
  // Trip type options
  const tripTypes = ref([
    { id: 'solo', label: 'Solo Trip' },
    { id: 'partner', label: 'Partner Trip' },
    { id: 'friends', label: 'Friends Trip' },
    { id: 'family', label: 'Family Trip' }
  ]);
  
  // State for selected trip type
  const selectedTripType = ref(null);
  
  // Method to select trip type
  const selectTripType = (typeId) => {
    selectedTripType.value = typeId;
  };
  
  const goBack = () => {
  router.back();  // Go to the previous page
};
  // Proceed to the next step
  const goToNextStep = () => {
  const { start, end, countryCode } = router.currentRoute.value.query; // Receive previous data
  console.log('passing info to tags.vue:', start, end, countryCode );
  if (selectedTripType.value) {
    router.push({
      name: 'TagsPage',
      query: {
        start,
        end,
        countryCode,
        tripType: selectedTripType.value,
      }
    });
  } else {
    console.log('Please select a trip type.');
  }
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
  
  /* Trip options styling */
  .trip-options {
    display: flex;
    gap: 10px;
    margin-top: 20px;
  }
  
  button.selected {
    background-color: #4caf50;
    color: white;
  }
  
  .actions {
    margin-top: 20px;
    text-align: center;
  }
  
  button {
    padding: 10px 20px;
    background-color: #ddd;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #ccc;
  }
  </style>