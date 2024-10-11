<template>
    <div v-if="videoInfo">
      <h2>Video Information</h2>
      <p><strong>Title:</strong> {{ videoInfo.title }}</p>
      <p><strong>Author:</strong> {{ videoInfo.author }}</p>
      <p><strong>Play Count:</strong> {{ videoInfo.play_count }}</p>
      <p><strong>Likes:</strong> {{ videoInfo.likes }}</p>
      <p><strong>Comments Count:</strong> {{ videoInfo.comments_count }}</p>
    </div>
    
    <div v-if="locationInfo">
      <h3>Location Information</h3>
      <p><strong>Place:</strong> {{ locationInfo.place_name }}</p>
      <p><strong>Country:</strong> {{ locationInfo.country }}</p>
      <p><strong>City:</strong> {{ locationInfo.city }}</p>
      <p><strong>Latitude:</strong> {{ locationInfo.coordinates.latitude }}</p>
      <p><strong>Longitude:</strong> {{ locationInfo.coordinates.longitude }}</p>
    </div>

    <div v-if="relatedPlaces.length">
      <h2>Related Places:</h2>
      <ul>
        <li v-for="place in relatedPlaces" :key="place.place_name">
          <strong>{{ place.place_name }}</strong> - {{ place.activities.join(', ') }} <br/>
          <strong>Country:</strong> {{ place.country }} <br/>
          <strong>City:</strong> {{ place.city }} <br/>
          <strong>Coordinates:</strong> ({{ place.coordinates.latitude }}, {{ place.coordinates.longitude }}) <br/>
          <strong>Image:</strong><br/>
          <img :src="place.place_png" alt="Image of {{ place.place_name }}" width="300px"/>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        videoInfo: null, // To hold video info data
        relatedPlaces: [] // To hold related places data
      };
    },
    mounted() {
      // Parse the passed data from the query params
      this.videoInfo = JSON.parse(this.$route.query.videoInfo);
      this.relatedPlaces = JSON.parse(this.$route.query.relatedPlaces);
      this.locationInfo = JSON.parse(this.$route.query.locationInfo);
    }
  };
  </script>
  
  <style scoped>
  /* Add any styles if needed */
  </style>