<template>
    <div class="progress-container">
        <div class="progress-bar" :style="{ width: progress + '%' }"></div>
    </div>
    <div class="calendar-page-layout">
        <!-- Centered Title -->
        <div class="title-wrapper">
            <a class="navbar-brand" href="#">
                <h1 id="title" class="h1">wander.</h1>
            </a>
        </div>

        <div class="content-wrapper">
            <!-- Left Image Card Section -->
            <div class="image-card">
                <img src="@/assets/background_header.jpeg" alt="Travel Background" class="image-card-content" />
                <div class="image-card-overlay">
                    <h1>Your Journey Begins Now.</h1>
                </div>
            </div>

            <!-- Right Form Section -->
            <div class="form-section">
        <!-- Header Text -->
        <h2 class="form-header">What kind of trip are you planning?</h2>

        <!-- Trip Type Options -->
        <div class="trip-options">
          <button v-for="type in tripTypes" :key="type.id"
                  :class="{ 'selected': selectedTripType === type.id }"
                  @click="selectTripType(type.id)">
            {{ type.label }}
          </button>
        </div>

        <!-- Country Selection Dropdown -->
        <div class="country-selection">
          <label for="country">Where do you want to go?</label>
          <select v-model="selectedCountry" id="country">
            <option disabled value="">Please select a country</option>
            <option v-for="(country, index) in countries" :key="index" :value="country.code">
              {{ country.name }} ({{ country.code }})
            </option>
          </select>
        </div>

        <!-- Action Buttons -->
        <div class="action-buttons">
            <button class="btn-back" @click="goBack">
      <span class="arrow">←</span>
    </button>
          <button class="btn-next" @click="goToNextStep">Continue</button>
        </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import router from '@/router';
import { countries } from '@/countries.js';

// Progress bar state
const progress = ref(25);  // Set to the starting progress for the first step

// Trip type options
const tripTypes = ref([
    { id: 'solo', label: 'Solo Trip' },
    { id: 'partner', label: 'Partner Trip' },
    { id: 'friends', label: 'Friends Trip' },
    { id: 'family', label: 'Family Trip' }
]);

// State for selected trip type and country
const selectedTripType = ref(null);
const selectedCountry = ref('');

// Method to select trip type
const selectTripType = (typeId) => {
    selectedTripType.value = typeId;
};

const goBack = () => {
    router.back();
  };

// Proceed to the next step
const goToNextStep = () => {
    if (selectedTripType.value && selectedCountry.value) {
        console.log("Navigating to CalendarPage with the following data:");
        console.log("Trip Type:", selectedTripType.value);
        console.log("Country Code:", selectedCountry.value);

        router.push({
            name: 'CalendarPage',
            query: {
                tripType: selectedTripType.value,
                countryCode: selectedCountry.value,
            },
        });
    } else {
        alert('Please select a trip type and a country.');
    }
};
</script>

<style scoped>
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
/* Parent Layout */
.calendar-page-layout {
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

/* Content Wrapper for Left and Right Sections */
.content-wrapper {
    display: flex;
    width: 100%;
    max-width: 1600px;
    gap: 2rem;
    height: 100%; /* Ensures both sections fill the vertical space */
    align-items: stretch; /* Stretches both child elements to fill equal height */
}

/* Left Image Card */
.image-card {
    flex: 1 1 50%; /* Allows it to expand to fill available space */
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
    top: 50px; /* Adjust the vertical position as needed */
    left: 20px;
    color: white;
    text-align: left;
    padding: 1rem;
    border-radius: 1rem;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    max-width: 50%; /* Limit width so text doesn’t go all the way across */
}

.image-card-overlay h1 {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
    margin: 0;
}

.form-section {
  flex: 1 1 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 2rem 5rem 5rem 10rem;
  text-align: left;
}

/* Header */
.form-header {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

/* Trip Options */
.trip-options {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.trip-options button {
  padding: 0.5rem 1rem;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
}

.trip-options button.selected {
  background: linear-gradient(90deg, #44c7f4, #3dd598);
  color: white;
}

/* Country Selection */
.country-selection {
  margin-bottom: 1.5rem;
}

.country-selection label {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  display: block;
}

.country-selection select {
  width: 70%;
  padding: 0.5rem;
  font-size: 1rem;
  border-radius: 4px;
  border: 1px solid #ccc;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.btn-back {
  width: 40px;
  height: 40px;
  border: 2px solid #ccc; /* Border color */
  border-radius: 50%; /* Make it circular */
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  cursor: pointer;
  transition: border-color 0.3s;
}

.btn-back:hover {
  border-color: #888; /* Darken border on hover */
}

.arrow {
  font-size: 1.2rem; /* Arrow size */
  color: #333; /* Arrow color */
}

.btn-next {
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

.btn-next:hover {
  transform: scale(1.05); /* Slightly enlarge on hover */
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); /* Shadow on hover */
}

.action-buttons {
  display: flex;
  align-items: center;
}

/* Responsive */
@media screen and (max-width: 768px) {
  .content-wrapper {
    flex-direction: column;
  }
  .form-section {
    padding: 1rem 2rem;
  }
}
</style>