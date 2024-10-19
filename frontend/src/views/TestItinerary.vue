<template>
  <div class="generated-itinerary">
    <div class="container">
      <div class="row justify-content-between align-items-center sticky-header g-0 m-2">
        <!-- Header section -->
        <div class="col-12 date-column">
          <h2>My Itinerary</h2>
        </div>
      </div>

      <!-- Show message if no itinerary is generated -->
      <div v-if="!itineraryGenerated" class="empty-message">
        <p>No itinerary generated. Go to 
          <router-link to="/savedplaces">saved places</router-link> 
          and add places.
        </p>
      </div>

      <!-- Render the itinerary if generated -->
      <div v-else class="row justify-content-center">
        <div class="col-lg-12"> <!-- Make the itinerary 8 out of 12 columns on larger screens -->
          <div v-for="(day, index) in itinerary" :key="index" class="day-container">
            <h3 class="day-header">Day {{ index + 1 }}</h3>
            <div class="row day-itinerary">
              <!-- Time column -->
              <div class="col-lg-3 time-column">
                <p v-for="(time, timeIndex) in times" :key="timeIndex">{{ time }}</p>
              </div>

              <!-- Places and activities column -->
              <div class="col-lg-9 activity-column">
                <ul>
                  <li v-for="(place, placeIndex) in day" :key="placeIndex">
                    {{ place.name }} - {{ place.vicinity || 'No description available' }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

export default {
  name: "GeneratedItinerary",
  setup() {
    const route = useRoute();
    const itineraryGenerated = ref(false);
    const itinerary = ref([]);
    
    // Dummy times to display next to the activities
    const times = ['09:00 am', '11:00 am', '02:00 pm', '04:00 pm'];

    onMounted(() => {
      console.log("Route Query:", route.query);

      if (route.query.itineraryGenerated) {
        itineraryGenerated.value = route.query.itineraryGenerated === 'true';
        console.log("Itinerary Generated:", itineraryGenerated.value);

        if (route.query.itinerary) {
          try {
            itinerary.value = JSON.parse(route.query.itinerary);
            console.log("Itinerary Data:", itinerary.value); // Log the itinerary data
          } catch (error) {
            console.error("Error parsing itinerary data:", error);
          }
        }
      }
    });

    return { itineraryGenerated, itinerary, times };
  }
};
</script>

<style scoped>
.generated-itinerary {
  font-family: 'Roboto', sans-serif;
  padding: 20px;
}

.sticky-header {
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 1000;
  padding: 10px 5%;
  border-bottom: 1px solid lightgrey;
}

.date-column {
  text-align: left;
  padding-left: 5%;
  white-space: nowrap;
  font-size: 1.8rem;
  font-weight: bold;
}

.empty-message {
  text-align: center;
  font-size: 1.2rem;
  color: gray;
  padding: 20px;
}

/* Day container for each day */
.day-container {
  margin-bottom: 30px;
  padding: 15px;
  border-radius: 8px;
  background-color: #f9fbff; /* Light blue */
  border: 1px solid #d8e2f1;
}

/* Header for each day */
.day-header {
  background-color: #e6f0fa;
  padding: 10px;
  font-size: 1.8rem;
  text-align: center;
  font-weight: bold;
  border-radius: 8px;
  margin-bottom: 20px;
  border: 1px solid #d1e0f0;
}

.day-itinerary {
  display: flex;
  background-color: #f0f8ff;
  padding: 15px;
  border-radius: 10px;
}

/* Time column with right alignment */
.time-column {
  text-align: right;
  font-weight: bold;
  font-size: 1rem;
  color: #333;
  padding-right: 15px;
  line-height: 2.5;
}

/* Activity/places column */
.activity-column ul {
  list-style: none;
  padding: 0;
}

.activity-column li {
  padding: 10px 0;
  font-size: 1.1rem;
  border-bottom: 1px solid #ddd;
}

.activity-column li:last-child {
  border-bottom: none;
}

/* Ensure each day block and time column are separated */
.row {
  margin: 0;
  display: flex;
}

.col-3, .col-9 {
  padding-left: 10px;
  padding-right: 10px;
}

@media (max-width: 768px) {
  /* Stack columns for mobile */
  .day-itinerary {
    flex-direction: column;
  }

  .time-column {
    text-align: left;
    padding-right: 0;
    margin-bottom: 10px;
  }
}
</style>