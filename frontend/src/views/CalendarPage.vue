<template>
    <div class="calendar-page">
      <!-- Progress Bar -->
      <div class="progress-container">
        <div class="progress-bar" :style="{ width: progress + '%' }"></div>
        <p>{{ progressText }}</p>
      </div>
  
      <!-- Country Selection Dropdown -->
      <div class="country-selection">
        <label for="country">Select Your Country:</label>
        <select v-model="selectedCountry" id="country">
          <option disabled value="">Please select a country</option>
          <option v-for="(country, index) in countries" :key="index" :value="country.code">
            {{ country.name }} ({{ country.code }})
          </option>
        </select>
      </div>
  
      <!-- Calendar Component with Range Selection and Drag Feature -->
      <VDatePicker
        v-model.range="range"
        :select-attribute="selectDragAttribute"
        :drag-attribute="selectDragAttribute"
        @drag="dragValue = $event"
      >
        <template #day-popover="{ format }">
          <div class="text-sm">
            {{ format(dragValue ? dragValue.start : range.start, 'MMM D') }} -
            {{ format(dragValue ? dragValue.end : range.end, 'MMM D') }}
          </div>
        </template>
      </VDatePicker>
  
      <!-- Date Summary -->
      <div class="date-summary" v-if="range.start && range.end">
        <h3>Selected Dates</h3>
        <p>From: {{ formatDate(range.start) }}</p>
        <p>To: {{ formatDate(range.end) }}</p>
      </div>
  
      <!-- Tips Section -->
      <div class="tips">
        <h4>Tips for selecting dates</h4>
        <ul>
          <li>Choose a start and end date for your trip.</li>
          <li>You can select a range of consecutive dates.</li>
          <li>Make sure your dates don't overlap with previous plans.</li>
        </ul>
      </div>
  
      <!-- Action Button -->
      <div class="actions">
        <button class="btn-secondary" @click="goBack">Back</button>
        <button class="btn-primary" @click="goToNextStep">Next Step</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import router from '@/router';
  import { ref, computed } from 'vue';
  import { countries } from '@/countries.js';
  
  // Date range and drag values
  const range = ref({
    start: new Date(),
    end: new Date(),
  });
  const dragValue = ref(null);
  const selectDragAttribute = computed(() => ({
    popover: {
      visibility: 'hover',
      isInteractive: false,
    },
  }));
  
  // Country selection (name and code)
  const selectedCountry = ref('');
  
  // Progress and step details
  const progress = ref(25);
  const progressText = ref('Step 1 of 4: Choose Dates');
  
  // Date formatting function
  const formatDate = (date) => {
    return new Date(date).toLocaleDateString();
  };
  
  // Navigation functions
  const goBack = () => {
    router.back(); // Go to the previous page
  };
  
  const goToNextStep = () => {
    if (!selectedCountry.value) {
      alert('Please select a country.');
      return;
    }
  
    if (range.value.start && range.value.end && new Date(range.value.start) <= new Date(range.value.end)) {
      console.log('Country Code:', selectedCountry.value);
      console.log('Start Date:', range.value.start);
      console.log('End Date:', range.value.end);
  
      router.push({
        name: 'TrvPartner',
        query: {
          start: range.value.start,
          end: range.value.end,
          countryCode: selectedCountry.value, // Pass selected country code
        },
      });
    } else {
      console.log('Please select a valid date range.');
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
  
  /* Country dropdown styling */
  .country-selection {
    margin: 20px 0;
  }
  
  .country-selection select {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    border-radius: 5px;
    border: 1px solid #ccc;
  }
  
  /* Calendar and other styling */
  .calendar-page {
    max-width: 60%;
    margin: 0 auto;
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 10px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .date-summary {
    margin-top: 20px;
  }
  
  .tips {
    margin-top: 20px;
  }
  
  .actions {
    margin-top: 20px;
    text-align: center;
  }
  
  button {
    padding: 10px 20px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }
  </style>