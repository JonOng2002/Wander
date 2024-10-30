<template>
    <div class="overlay-skeleton">
      <AppNavbar class="sticky-top" /> <!-- Navbar -->
  
      <!-- Central GlobeLoader -->
      <div class="loading-overlay">
        <GlobeLoader :message="message" size="5rem" />
      </div>
  
      <!-- Main Content Skeleton Layout -->
      <div class="content row g-0">
        <!-- Left Side: Skeleton Cards for Itinerary Details -->
        <div class="col-md-6 col-12 itinerary-details-container">
          <div class="itinerary-details">
            <!-- Skeleton Header -->
            <div class="date-column skeleton-heading">
              <div class="skeleton skeleton-heading-text"></div>
              <div class="skeleton skeleton-heading-subtext"></div>
            </div>
            <!-- Skeleton Save Button -->
            <div class="skeleton-save-button"></div>
  
            <!-- Day Section Skeletons -->
            <div class="day-section-skeleton" v-for="n in 3" :key="n">
              <div class="skeleton skeleton-day-header"></div>
              <div class="skeleton skeleton-day-description"></div>
              <div class="itinerary-table-skeleton">
                <div class="itinerary-row-skeleton" v-for="m in 2" :key="m">
                  <div class="skeleton skeleton-time"></div>
                  <div class="skeleton skeleton-place-column">
                    <div class="skeleton skeleton-image"></div>
                    <div class="skeleton skeleton-activity-name"></div>
                    <div class="skeleton skeleton-location"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Right Side: Skeleton Map -->
        <div class="col-md-6 col-12 skeleton-map-container">
          <div class="skeleton-map"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue';
  import GlobeLoader from '@/components/GlobeLoader.vue';
  
  const message = ref("Generating your itinerary...");
  const loadingMessages = [
    "Generating your itinerary...",
    "Fetching data from OpenAI...",
    "Fetching from PlacesAPI...",
    "Finalizing your itinerary details...",
    "Almost done! Just a moment..."
  ];
  
  let messageIndex = 0;
  let messageInterval = null;
  
  const startMessageRotation = () => {
    const displayDuration = 2500;
    messageInterval = setInterval(() => {
      message.value = loadingMessages[messageIndex];
      messageIndex = (messageIndex + 1) % loadingMessages.length;
    }, displayDuration);
  };
  
  onMounted(() => {
    startMessageRotation();
  });
  
  onBeforeUnmount(() => {
    clearInterval(messageInterval);
  });
  </script>
  
  <style scoped>
  /* Full-page overlay style */
  .overlay-skeleton {
    position: relative;
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
  }
  
  /* Navbar */
  .sticky-top {
    top: 0;
    position: sticky;
    z-index: 1020;
    background-color: black;
  }
  
  /* Loading overlay for GlobeLoader */
  .loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.85);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
  }
  
  /* Left Side Skeleton Styling */
  .date-column.skeleton-heading {
    padding: 10px 20px;
    background-color: #f8f9fa;
    margin-bottom: 20px;
  }
  .skeleton-heading-text {
    width: 70%;
    height: 20px;
    background-color: #ccc;
    border-radius: 5px;
    margin-bottom: 8px;
  }
  .skeleton-heading-subtext {
    width: 50%;
    height: 18px;
    background-color: #ddd;
    border-radius: 5px;
  }
  
  /* Save Button Skeleton */
  .skeleton-save-button {
    width: 120px;
    height: 35px;
    background-color: #ddd;
    border-radius: 5px;
    margin-bottom: 20px;
    margin-left: 20px;
  }
  
  /* Day Section Skeletons */
  .day-section-skeleton {
    padding: 20px;
    background-color: #fdfdfd;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
  }
  
  .skeleton-day-header {
    width: 70%;
    height: 25px;
    background-color: #ccc;
    border-radius: 5px;
    margin-bottom: 10px;
  }
  
  .skeleton-day-description {
    width: 90%;
    height: 18px;
    background-color: #ddd;
    border-radius: 5px;
    margin-bottom: 15px;
  }
  
  .itinerary-table-skeleton {
    padding: 15px;
    background-color: #f0f0f0;
    border-radius: 10px;
  }
  
  .itinerary-row-skeleton {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
  }
  
  .skeleton-time {
    width: 40px;
    height: 20px;
    background-color: #ccc;
    border-radius: 5px;
    margin-right: 15px;
  }
  
  .skeleton-place-column {
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;
  }
  
  .skeleton-image {
    width: 100%;
    height: 80px;
    background-color: #e0e0e0;
    border-radius: 8px;
  }
  
  .skeleton-activity-name,
  .skeleton-location {
    height: 20px;
    background-color: #ddd;
    border-radius: 5px;
    width: 80%;
  }
  
  /* Right Side Skeleton Map Style */
  .skeleton-map-container {
    background-color: #f8f9fa;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .skeleton-map {
    width: 90%;
    height: 90%;
    background-color: #c0c0c0;
    border-radius: 10px;
  }
  </style>