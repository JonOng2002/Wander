<template>
  <div class="generated-itinerary">
    <div class="row justify-content-between align-items-center sticky-header g-0 m-2">
      <!-- Date Column -->
      <div class="col-3 date-column">
        <h1>Your Itinerary</h1>
      </div>
    </div>
    <div v-if="!itineraryGenerated" class="empty-message">
      <p>
        No itinerary generated. Go to 
        <router-link to="/savedplaces">saved pages</router-link> 
        and add places.
      </p>
    </div>
    <div v-else>
      <div v-for="(day, index) in staticItinerary" :key="index">
        <h2>Day {{ index + 1 }}</h2>
        <ul>
          <li v-for="(place, placeIndex) in day" :key="placeIndex">
            {{ place.name }} - {{ place.description }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "GeneratedItinerary",
  props: {
    itineraryGenerated: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      staticItinerary: [
        [
          { name: 'Place 1', description: 'Description 1' },
          { name: 'Place 2', description: 'Description 2' },
          { name: 'Place 3', description: 'Description 3' }
        ],
        [
          { name: 'Place 4', description: 'Description 4' },
          { name: 'Place 5', description: 'Description 5' },
          { name: 'Place 6', description: 'Description 6' }
        ],
        [
          { name: 'Place 7', description: 'Description 7' },
          { name: 'Place 8', description: 'Description 8' },
          { name: 'Place 9', description: 'Description 9' }
        ]
      ]
    };
  }
};
</script>

<style scoped>
.generated-itinerary {
  text-align: center;
  padding: 20px;
  font-family: 'Roboto', sans-serif;
}
.empty-message {
  color: #888;
  font-size: 1.2em;
}
</style>