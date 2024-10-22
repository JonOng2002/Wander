<template>
  <div class="gen-itinerary-page">
    <h2>Generated Itinerary</h2>

    <!-- Loading Animation -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Generating itinerary...</p>
    </div>

    <!-- Itinerary Summary -->
    <div v-if="!loading && itinerary">
      <h3>Itinerary Summary</h3>
      <p>{{ itinerary.itinerary_summary }}</p>

      <!-- Day by Day Itineraries -->
      <div v-for="(day, index) in itinerary.day_by_day_itineraries" :key="index" class="day-itinerary">
        <h4>Day {{ day.day }} - {{ day.date }}</h4>
        <p>{{ day.summary }}</p>

        <ul>
          <li v-for="(activity, actIndex) in day.activities" :key="actIndex">
            <strong>{{ activity.time }}:</strong> {{ activity.activity_name }} <br>
            <em>Location:</em> {{ activity.location.name }} <br>
            <em>Description:</em> {{ activity.description }} <br>
            <em>Coordinates:</em> Latitude: {{ activity.location.coordinates.latitude }}, Longitude: {{ activity.location.coordinates.longitude }}
          </li>
        </ul>
      </div>
    </div>

    <!-- No Itinerary Found Message -->
    <div v-if="!loading && !itinerary">
      <p>No itinerary found. Please try again.</p>
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <!-- Back and Retry Buttons -->
    <div class="actions">
      <button @click="goBack">Back</button>
      <button v-if="!loading" @click="submitData">Retry</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import router from '@/router';

// Initialize states
const itinerary = ref(null);  // Initialized as null
const loading = ref(false);
const errorMessage = ref(null);

const goBack = () => {
  router.back();
};

// Fetch itinerary from backend (Flask)
const submitData = async () => {
  const { start, end, tripType, itinerary: itineraryData, selectedTags } = router.currentRoute.value.query;

  const dataToSend = {
    startDate: start,
    endDate: end,
    tripType,
    itinerary: JSON.parse(itineraryData),
    tags: JSON.parse(selectedTags)  // Tags are parsed here
  };

  loading.value = true;
  errorMessage.value = null;

  try {
    const response = await axios.post("http://127.0.0.1:5000/generate-itinerary", dataToSend, {
      headers: {
        "Content-Type": "application/json",
      },
      withCredentials: false
    });
    
    // Assign the response data to the itinerary ref
    itinerary.value = response.data;

  } catch (error) {
    errorMessage.value = 'Failed to generate itinerary.';
    console.error(error);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.gen-itinerary-page {
  text-align: center;
  margin: 20px;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-radius: 50%;
  border-top: 4px solid #4caf50;
  width: 30px;
  height: 30px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.day-itinerary {
  margin: 20px 0;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin: 10px 0;
}

.error-message {
  color: red;
  margin-top: 20px;
}

.actions {
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 10px;
}

button:hover {
  background-color: #45a049;
}
</style>