<template>
  <div class="itinerary-page">
    <div class="row justify-content-between align-items-center sticky-header g-0 m-2">
      <!-- Date Column -->
      <div class="col-3 date-column">
        <h2>8 October 2024</h2>
      </div>
      <!-- Additional content can go in the next columns if necessary -->
       <div class="col-auto generateButton">
        <button @click="navigateToGeneratedItinerary" type="button" class="btn btn-primary">Generate Itinerary!</button>
       </div>
    </div>

      <!-- BS card: Start -->
      <div class="row card-row justify-content-start g-0">
        <div class="card-container">
          <div class="card destination-card">
            <img src="@/assets/mountfuji.png" class="card-img-side" alt="..." />
            <div class="card-body">
              <h5 class="card-title">Mount Fuji</h5>
              <p class="card-text">
                Standing at 3,776 meters, Mt. Fuji is the tallest peak in Japan, the result of volcanic activity that began approximately 100,000 years ago. Today, Mt. Fuji and the surrounding area are a popular recreational destination for hiking, camping and relaxation.
              </p>
              <p><button type="button" id="addToItinerary" class="btn">Add to Itinerary</button></p>
            </div>
          </div>
        </div>
      </div>
      <!-- BS card: End -->

      <!-- BS card: Start -->
      <div class="row justify-content-start g-0">
        <div class="card-container">
          <div class="card destination-card">
            <img src="@/assets/tokyotower.jpg" class="card-img-side" alt="..." />
            <div class="card-body">
              <h5 class="card-title">Tokyo Tower</h5>
              <p class="card-text">
                Tokyo Tower was erected in 1958 as a broadcasting tower. It controls broadcast signals for television, FM radio transmission and reception, and traffic information transmission in the Tokyo metropolitan area. 
              </p>
              <p><button type="button" id="addToItinerary" class="btn">Add to Itinerary</button></p>
            </div>
          </div>
        </div>
      </div>
      <!-- BS card: End -->

      <!-- BS card: Start -->
      <div class="row justify-content-start g-0">
        <div class="card-container">
          <div class="card destination-card">
            <img src="@/assets/shibuyacrossing.jpg" class="card-img-side" alt="..." />
            <div class="card-body">
              <h5 class="card-title">Shibuya Crossing</h5>
              <p class="card-text">
                Shibuya Crossing is one of Tokyo's most recognizable sights, pictured in countless films, magazines and blogs. During its busiest times, an estimated 1,000 to 2,500 people forge their way across this intersection every two minutes, enough to quickly fill up a football stadium.
              </p>
              <p><button type="button" id="addToItinerary" class="btn">Add to Itinerary</button></p>
            </div>
          </div>
        </div>
      </div>
      <!-- BS card: End -->

      <!-- BS card: Start -->
      <div class="row justify-content-start g-0">
        <div class="card-container">
          <div class="card destination-card">
            <img src="@/assets/meiji_jingu.jpg" class="card-img-side" alt="..." />
            <div class="card-body">
              <h5 class="card-title">Meiji Jingu</h5>
              <p class="card-text">
                
                Meiji Jingu is one of the Shinto shrines in Japan, with the vast land of the forest (70 ha.), located in the middle of the megacity, Tokyo. Once you step into this precinct, you will forget that you are in the hustle bustle city, and will find Japanese traditional scene amidst greenery nature.
              </p>
              <p><button type="button" id="addToItinerary" class="btn">Add to Itinerary</button></p>
            </div>
          </div>
        </div>
      </div>
      <!-- BS card: End -->
    </div>
  
</template>

<script>
export default {
  name: "ItineraryPage",
  methods: {
    navigateToGeneratedItinerary() {
      this.$router.push( { name: 'GeneratedItinerary' } );
    },
  },
};
</script>

<style scoped>
.itinerary-page {
  font-family: "Roboto", sans-serif;
  margin: 0;
  padding: 0;
}

/* Ensure the header is sticky */
.sticky-header {
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 1000;
  padding: 10px 5%;
  border-bottom: 1px solid lightgrey;
}

/* Ensure the date column is pushed to the left */
.date-column {
  text-align: left;
  padding-left: 5%;
  padding-right: 0;
  white-space: nowrap;
  font-size: 1.5rem;
  margin-top: 10px;
  margin-bottom: 10px;
}

.generateButton {
    text-align: right;
    padding-right: 5%;
    padding-left: 0;
    white-space: nowrap;
    font-size: 1.5rem;
    margin-top: 10px;
    margin-bottom: 10px;
}
/* Reset or minimize row margin */
.row {
  margin-left: 0 !important;
  margin-right: 0 !important;
  margin-top: 3%;
}

.card-row {
  margin-top: 10px;
}

/* card container styles */
.card-container {
  padding-left: 5%;
  padding-right: 5%;
  margin-bottom: 10px;
}

/* card styles */
.destination-card {
  margin-left: 0;
  padding: 15px;
  height: auto; /* Set the height of the card to 30% of the viewport height */
  display: flex;
  justify-content: flex-start; /* Align card content to the left */
  align-items: center;
  flex-direction: row;
  overflow: hidden; /* Hide any overflow content */
  border-radius: 10px;
  ;
}

.card-img-side {
  width: 250px;
  max-height: 200px;
  object-fit: cover; /* Ensure the image fits within the card */
  margin-right: 15px;
}

.card-body {
  flex-grow: 1; /* Ensure the card text content takes up the rest of the space */
}

.card-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.card-text {
  font-size: 1rem;
  line-height: 1.4;
}

.btn {
    background-color: lightgray;
    color: black;
    border: 1px solid black;
}
</style>
