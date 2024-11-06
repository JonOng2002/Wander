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

              <!-- Country Selection with Multiselect -->
              <div class="country-selection">
                  <label for="country">Where do you want to go?</label>
                  <multiselect
                      v-model="selectedCountry"
                      :options="countries"
                      track-by="code"
                      label="name"
                      placeholder="Please select a country"
                      id="country"
                  ></multiselect>
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
import Multiselect from 'vue-multiselect';
import '@vueform/multiselect/themes/default.css'; // Import the default theme for Multiselect
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

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style scoped>
/* Your existing styles remain the same */

.progress-container {
width: 100%;
height: 10px;
overflow: hidden;
margin-top: 10px;
}

.progress-bar {
background-color: #3f94a7;
height: 100%;
transition: width 0.4s ease;
}

.calendar-page-layout {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
}

.title-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

#title {
  font-family: "Lobster Two", cursive;
  font-size: 2.5vw;
  color: #3f94a7;
}

.content-wrapper {
  display: flex;
  width: 100%;
  max-width: 1600px;
  gap: 2rem;
  height: 100%;
  align-items: stretch;
}

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
  top: 50px;
  left: 20px;
  color: white;
  text-align: left;
  padding: 1rem;
  border-radius: 1rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  max-width: 50%;
}

.image-card-overlay h1 {
  font-size: 2rem;
  font-weight: bold;
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

.form-header {
font-size: 1.5rem;
font-weight: bold;
margin-bottom: 1rem;
}

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
background: linear-gradient(90deg, #3f94a7, #6fb3d2);
color: white;
}

.country-selection {
margin-bottom: 1.5rem;
}

.country-selection label {
font-size: 1.5rem;
font-weight: bold;
margin-bottom: 0.5rem;
display: block;
}

/* Additional Styling for Multiselect */
.multiselect {
width: 70%;
text-align: left;
margin-left: 0;
}

.multiselect__option {
  color: #3f94a7; /* Desired color for option text */
}

.e-multiselect.e-input-group .e-input-group-icon, .e-multiselect.e-input-group.e-control-wrapper .e-input-group-icon:hover {
    color: #3f94a7; /* Desired color for dropdown icon */
    font-size: 14px;
}

.action-buttons {
display: flex;
gap: 0.5rem;
align-items: center;
}

.btn-back {
width: 40px;
height: 40px;
border: 2px solid #ccc;
border-radius: 50%;
display: flex;
align-items: center;
justify-content: center;
background-color: transparent;
cursor: pointer;
transition: border-color 0.3s;
}

.btn-back:hover {
border-color: #888;
}

.arrow {
font-size: 1.2rem;
color: #333;
}

.btn-next {
background: linear-gradient(90deg, #3f94a7, #6fb3d2);
color: white;
padding: 0.75rem 2rem;
border: none;
border-radius: 25px;
font-weight: bold;
cursor: pointer;
font-size: 1rem;
transition: transform 0.2s, box-shadow 0.2s;
margin-left: 1rem;
height: 50px;
flex-grow: 1;
max-width: 400px;
}

.btn-next:hover {
transform: scale(1.05);
box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

/* <=============== breakpoints and media =============>*/
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
  }
  .trip-options,.action-buttons{
    justify-content: center;
  }
}
</style>