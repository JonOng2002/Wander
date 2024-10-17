<template>
    <div class="generated-itinerary">
      <div class="row justify-content-between align-items-center sticky-header g-0 m-2">
        <!-- Header section -->
        <div class="col-3 date-column">
          <h2>My Itinerary</h2>
        </div>
      </div>

      <!-- Itinerary list -->
      <!-- <div v-if="itinerary.length === 0" class="empty-message">
        <p>No saved places found. Add more places!</p> -->
        
      





    </div>
  </template>
  
  <script>
  export default {
    name: "GeneratedItinerary",
    inject : ['itineraryState'],

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
  
  /* Empty message styles */
  .empty-message {
    text-align: center;
    font-size: 1.2rem;
    color: gray;
    padding: 20px;
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
    height: auto;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    flex-direction: row;
    overflow: hidden;
    border-radius: 10px;
  }
  
  .card-img-side {
    width: 250px;
    max-height: 200px;
    object-fit: cover;
    margin-right: 15px;
  }
  
  .card-body {
    flex-grow: 1;
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
  .btn:hover {
    background-color: darkgray; /* Slightly change color, but don't fade it out */
    color: black; /* Keep text color consistent */
  }
  
  /* Popup notification styles */
  .popup {
    position: fixed;
    top: 20px;
    right: 20px;
    background-color: #4caf50;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    font-weight: bold;
    z-index: 2000;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    transition: opacity 0.3s ease;
  }
  
  /* Itinerary list styles */
  .itinerary-list {
    margin-top: 20px;
  }
  
  .itinerary-list h3 {
    text-align: center;
  }
  
  .itinerary-list ul {
    list-style: none;
    padding: 0;
  }
  
  .itinerary-list li {
    margin: 10px 0;
    font-size: 1.2rem;
    text-align: center;
  }
  </style>
  