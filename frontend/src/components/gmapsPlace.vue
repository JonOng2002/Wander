<template>
    <GMapMap
      :center="center"
      :zoom="7"
      map-type-id="terrain"
      style="width: 100%; height: 400px"
    >
      <GMapCluster>
        <GMapMarker
          v-for="(m, index) in markers"
          :key="index"
          :position="m.position"
          :clickable="true"
          :draggable="true"
          @click="center=m.position"
        />
      </GMapCluster>
    </GMapMap>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  
  const center = ref({ lat: 51.093048, lng: 6.842120 }); // Default center of the map
  const markers = ref([]); // Empty marker list
  
  // Sample function to fetch saved places with coordinates
  const getSavedPlaces = async () => {
    // Here, you can fetch the saved places from Firebase or any backend
    // The data below is just an example
    const savedPlaces = [
      { lat: 51.093048, lng: 6.842120, name: 'Place 1' },
      { lat: 52.5200, lng: 13.4050, name: 'Place 2' }, // Berlin
      { lat: 48.8566, lng: 2.3522, name: 'Place 3' }, // Paris
    ];
  
    // Convert saved places into markers
    markers.value = savedPlaces.map(place => ({
      position: { lat: place.lat, lng: place.lng }
    }));
  };
  
  // Fetch the saved places when the component is mounted
  onMounted(() => {
    getSavedPlaces();
  });
  </script>
  
  <style scoped>
  /* Add any specific styles if needed */
  </style>