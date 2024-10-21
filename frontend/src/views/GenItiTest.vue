<template>
    <div class="gen-itinerary-page">
      <h2>Generated Itinerary</h2>
  
      <!-- Loading Animation -->
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <p>Generating itinerary...</p>
      </div>
  
      <!-- Itinerary Display -->
      <div v-if="!loading && itinerary.length">
        <ul>
          <li v-for="(item, index) in itinerary" :key="index">
            {{ item }}
          </li>
        </ul>
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
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import router from '@/router';
  
  const itinerary = ref([]);
  const loading = ref(false);
  const errorMessage = ref(null);
  
  // Fetch itinerary from backend (Flask)
  const submitData = async () => {
  const { start, end, tripType, itinerary: itineraryData, selectedTags } = router.currentRoute.value.query;

  console.log("Received Data:", {
    start,
    end,
    tripType,
    itinerary: JSON.parse(itineraryData),
    tags: JSON.parse(selectedTags),
  });
  
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
    const response = await axios.post('http://localhost:5000/generate-itinerary', dataToSend);
    itinerary.value = response.data.itinerary; // Assuming the response contains an itinerary array
  } catch (error) {
    errorMessage.value = 'Failed to generate itinerary.';
    console.error(error);
  } finally {
    loading.value = false;
  }
};
  
  const goBack = () => {
    router.back();
  };
  
  // Submit the data when the component mounts
  onMounted(() => {
    submitData();
  });
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