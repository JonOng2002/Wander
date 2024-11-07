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
          <button v-for="type in tripTypes" :key="type.id" :class="{ 'selected': selectedTripType === type.id }"
            @click="selectTripType(type.id)">
            {{ type.label }}
          </button>
        </div>

        <!-- Country Selection with Custom Searchable Dropdown -->
        <div class="country-selection">
          <label for="country">Where do you want to go?

          <div class="tooltip-container">
            <span class="question-mark" aria-label="Tooltip">
              <font-awesome-icon :icon="['fas', 'circle-info']" class="custom-icon" />
              <span class="tooltip-text">
                Select the same country where you saved places in your itinerary to ensure they match.
              </span>
            </span>
          </div>
        </label>
          <div class="searchable-dropdown" ref="dropdown">
            <input type="text" v-model="searchQuery" @focus="isDropdownOpen = true" @input="filterCountries"
              @keydown.down.prevent="navigateDown" @keydown.up.prevent="navigateUp"
              @keydown.enter.prevent="selectHighlighted" placeholder="Please select a country" id="country"
              class="country-input" />
            <ul v-if="isDropdownOpen && filteredCountries.length" class="dropdown-list">
              <li v-for="(country, index) in filteredCountries" :key="country.code"
                :class="{ 'highlighted': index === highlightedIndex }" @mousedown.prevent="selectCountry(country)"
                @mouseover="highlightedIndex = index">
                {{ country.name }}
              </li>
            </ul>
            <ul v-else-if="isDropdownOpen" class="dropdown-list no-results">
              <li>No countries found.</li>
            </ul>
          </div>
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
import { ref, onMounted, onBeforeUnmount } from 'vue';
import router from '@/router';
import { countries } from '@/countries.js';

// Progress bar state
const progress = ref(25); // Set to the starting progress for the first step

// Trip type options
const tripTypes = ref([
  { id: 'solo', label: 'Solo Trip' },
  { id: 'partner', label: 'Partner Trip' },
  { id: 'friends', label: 'Friends Trip' },
  { id: 'family', label: 'Family Trip' },
]);

// State for selected trip type and country
const selectedTripType = ref(null);
const searchQuery = ref('');
const isDropdownOpen = ref(false);
const filteredCountries = ref(countries);
const highlightedIndex = ref(-1);

// Reference to the dropdown container
const dropdown = ref(null);

// Method to select trip type
const selectTripType = (typeId) => {
  selectedTripType.value = typeId;
};

// Method to handle back navigation
const goBack = () => {
  router.back();
};

// Method to handle proceeding to the next step
const goToNextStep = () => {
  if (selectedTripType.value && searchQuery.value) {
    console.log("Navigating to CalendarPage with the following data:");
    console.log("Trip Type:", selectedTripType.value);
    console.log("Country Code:", searchQuery.value);

    router.push({
      name: 'CalendarPage',
      query: {
        tripType: selectedTripType.value,
        countryCode: searchQuery.value,
      },
    });
  } else {
    alert('Please select a trip type and a country.');
  }
};

// Method to filter countries based on search query
const filterCountries = () => {
  const query = searchQuery.value.toLowerCase();
  filteredCountries.value = countries.filter(country =>
    country.name.toLowerCase().includes(query)
  );
  highlightedIndex.value = -1; // Reset highlighted index
};

// Method to handle country selection
const selectCountry = (country) => {
  searchQuery.value = country.name;
  isDropdownOpen.value = false;
};

// Click outside handler to close dropdown
const handleClickOutside = (event) => {
  if (dropdown.value && !dropdown.value.contains(event.target)) {
    isDropdownOpen.value = false;
  }
};

// Keyboard navigation methods
const navigateDown = () => {
  if (filteredCountries.value.length === 0) return;
  if (highlightedIndex.value < filteredCountries.value.length - 1) {
    highlightedIndex.value += 1;
  }
};

const navigateUp = () => {
  if (filteredCountries.value.length === 0) return;
  if (highlightedIndex.value > 0) {
    highlightedIndex.value -= 1;
  }
};

const selectHighlighted = () => {
  if (highlightedIndex.value >= 0 && highlightedIndex.value < filteredCountries.value.length) {
    selectCountry(filteredCountries.value[highlightedIndex.value]);
  }
};

// Event listeners for clicks outside
onMounted(() => {
  document.addEventListener('mousedown', handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener('mousedown', handleClickOutside);
});
</script>

<style scoped>
/* Tooltip Container */
.tooltip-container {
  position: relative;
  display: inline-block;
  margin-left: 0.5rem; /* Adjust spacing between label and tooltip icon */
}

/* Tooltip Icon */
.question-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  background-color: #3f94a7;
  color: white;
  border-radius: 50%;
  font-size: 16px;
  cursor: pointer;
}

/* Tooltip Text */
.tooltip-container .tooltip-text {
  visibility: hidden;
  opacity: 0;
  width: 250px;
  background-color: #333;
  color: #fff;
  text-align: left;
  border-radius: 6px;
  padding: 10px;
  position: absolute;
  z-index: 10;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  transition: opacity 0.3s ease;
  margin-top: 5px; /* Adjust vertical spacing */
}

.tooltip-container .tooltip-text::after {
  content: "";
  position: absolute;
  top: -5px;
  left: 50%;
  transform: translateX(-50%);
  border-width: 5px;
  border-style: solid;
  border-color: transparent transparent #333 transparent;
}

/* Show Tooltip Text on Hover */
.tooltip-container:hover .tooltip-text {
  visibility: visible;
  opacity: 1;
}

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

.searchable-dropdown {
  position: relative;
  width: 70%;
}

.country-input {
  width: 100%;
  padding: 0.5rem 2rem 0.5rem 0.5rem;
  /* Extra padding for arrow */
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.country-input:focus {
  border-color: #3f94a7;
  outline: none;
}

.dropdown-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #ccc;
  border-top: none;
  background-color: white;
  z-index: 1000;
  border-radius: 0 0 4px 4px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 0;
  /* Remove padding around the dropdown */
  margin: 0;
  /* Remove margin around the dropdown */
}

.dropdown-list li {
  padding: 0.5rem;
  cursor: pointer;
  list-style-type: none;
  /* Removes the bullet points */
}

.dropdown-list li.highlighted,
.dropdown-list li:hover {
  background-color: #3f94a7;
  color: white;
}

.dropdown-list.no-results li {
  cursor: default;
  color: #999;
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
    align-items: center;
    /* Centers the contents vertically */
    justify-content: center;
    /* Centers the contents horizontally */
    gap: 2rem;
    max-height: 90vh;
    /* Limits the overall height of content-wrapper */
  }

  .form-section {
    height: auto;
    /* Allow form-section to expand naturally */
    padding: 1rem 1.5rem;
    /* Reduces excessive padding */
    margin: 0 auto;
    /* Ensures horizontal centering */
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
    width: 100%;
    /* Makes image-card take full width */
    max-width: 500px;
    /* Optional: restricts width to avoid excessive stretching */
    height: 40vh;
    /* Adjust height to fit smaller screens */
    max-height: 400px;
    /* Limit height to prevent excessive scrolling */
    margin: 0 auto;
    /* Centers the image card */
  }

  .form-section {
    width: 100%;
    /* Makes form-section take full width */
    max-width: 500px;
    /* Optional: restricts width to avoid excessive stretching */
    padding: 1rem;
    /* Adjust padding for better spacing on small screens */
    margin: 0 auto;
    /* Centers the form section */
    height: auto;
    /* Allow natural expansion */
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

  .trip-options,
  .action-buttons {
    justify-content: center;
  }
}
</style>