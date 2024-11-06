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
        <img src="@/assets/calendarPage.jpg" alt="Travel Background" class="image-card-content" />
        <div class="image-card-overlay">
          <h1>Dream. Plan. Depart.</h1>
        </div>
      </div>

      <!-- Right Form Section -->
      <div class="form-section">
        <!-- Calendar Component -->
        <h2 class="calendar-header">Select Your Travel Dates</h2>
<p class="calendar-subtext">Choose a date range to plan your next adventure.</p>
        <VDatePicker transparent borderless expanded v-model.range="range" :columns="columns" :min-date="today" :disabled-dates="disablePastDates"
          :select-attribute="selectDragAttribute">
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
          <p id="startDate">From: {{ formatDate(range.start) }}</p>
          <p id="endDate">To: {{ formatDate(range.end) }}</p>
        </div>

        <!-- Action Buttons -->
        <div class="action-buttons">
          <button class="btn-back" @click="goBack">←</button>
          <button class="btn-primary" @click="goToNextStep">Continue</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import router from '@/router';
import { ref, computed, nextTick, onMounted } from 'vue';
import { useScreens } from 'vue-screen-utils';
const { mapCurrent } = useScreens({ xs: '0px', sm: '640px', md: '768px', lg: '1024px' });
const columns = mapCurrent({ lg: 2 }, 1);

const { countryCode, tripType } = router.currentRoute.value.query;

const today = new Date();
today.setDate(today.getDate() - 1);

const disablePastDates = ref([{ start: null, end: today }]);


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

const progress = ref(50);

const formatDate = (date) => {
  return new Date(date).toLocaleDateString();
};

const goBack = () => {
  router.back();
};

const goToNextStep = () => {
  if (range.value.start && range.value.end) {
    router.push({
      name: 'TagsPage',
      query: {
        start: range.value.start,
        end: range.value.end,
        countryCode,
        tripType,
      },
    });
  } else {
    alert('Please select a valid date range.');
  }
};

onMounted(async () => {
  await nextTick();
  console.log("Received data in CalendarPage:");
  console.log("Trip Type:", tripType);
  console.log("Country Code:", countryCode);
});
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
  top: 43%;
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
  backdrop-filter: blur(1px);
}

.image-card-overlay h1 {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  margin: 0;
}

/* Right Form Section */
.form-section {
  flex: 1 1 50%;
  background-color: transparent;
  padding: 1rem 3rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  height: 80vh;
  text-align: left;
  width: 100%;
}



.calendar-header {
  font-size: 1.5rem; /* Smaller font size for compactness */
  font-weight: bold;
  margin-bottom: 0.5rem; /* Reduced margin */
  padding-left: 0.5rem;
  color: #333;
}

.calendar-subtext {
  font-size: 0.9rem; /* Smaller font size for subtext */
  margin-bottom: 1rem; /* Reduced space below */
  padding-left: .5rem;
  color: #666;
}
/* Date Summary Styling */
.date-summary {
  margin-top: 0%;
  padding: 0.2rem;
  width: 100%;
  font-size: 0.9rem;
}

.date-summary h3 {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 0;
  padding-left: .5rem;
  padding-bottom: .5rem;
}

#startDate,
#endDate {
  font-weight: bold;
  color: #2a5ead;
  padding: 0rem .5rem 0rem .5rem;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
}

/* Back Button - Circular Arrow */
.btn-back {
  width: 50px;
  height: 50px;
  border: 2px solid #ccc;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  cursor: pointer;
  transition: border-color 0.3s;
  font-size: 1.2rem; /* For arrow icon */
  color: #333;
}

.btn-back:hover {
  border-color: #888;
}

/* Next Button - Gradient Background */
.btn-primary {
  background: linear-gradient(90deg, #4a90e2, #8e44ad);
  height: 50px;
  color: white;
  padding: 0.5rem 3rem;
  margin-left: 2rem;
  border: none;
  border-radius: 25px;
  font-weight: bold;
  cursor: pointer;
  font-size: 1rem;
  transition: transform 0.2s, box-shadow 0.2s;
  flex-grow: 1; /* Allow the button to expand to available space */
  max-width: 400px;
}

.btn-primary:hover {
  transform: scale(1.05);
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

/* Responsive Adjustments */
@media screen and (max-width: 768px) {
  .content-wrapper {
    flex-direction: column;
  }

  .form-section {
    padding: 1rem 2rem;
    height: auto;
  }

  .btn-primary {
    width: auto;
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

  .action-buttons{
    justify-content: center;
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
}
</style>