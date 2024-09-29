<template>
  <div id="app">
    <h1>TikTok Comment Fetcher</h1>
    
    <!-- Input field for the TikTok link -->
    <input v-model="tiktokLink" placeholder="Paste TikTok link here" />
    <button @click="fetchComments">Get Comments</button>
    
    <!-- Display the comments -->
    <div v-if="comments.length">
      <h2>Comments:</h2>
      <ul>
        <li v-for="(comment, index) in comments" :key="index">
          <strong>{{ comment.user.nickname }}:</strong> {{ comment.text }} (Likes: {{ comment.digg_count }})
        </li>
      </ul>
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage">{{ errorMessage }}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      tiktokLink: '', // To store the user's input (TikTok link)
      comments: [], // To store the fetched comments
      errorMessage: '', // To store any error messages
    };
  },
  methods: {
    // Function to extract TikTok video ID from the URL
    extractVideoId(link) {
      const regex = /\/video\/(\d+)\?/; // This regex extracts the video ID from the link
      const match = link.match(regex);
      return match ? match[1] : null; // Return the video ID if found, otherwise null
    },
    
    // Function to fetch comments from the backend
    async fetchComments() {
      const videoId = this.extractVideoId(this.tiktokLink); // Extract the video ID from the link
      
      if (videoId) {
        try {
          // Make an API call to the Flask backend
          const response = await axios.get(`http://127.0.0.1:5000/comments/${videoId}`);
          this.comments = response.data; // Store the fetched comments in the Vue data
          this.errorMessage = ''; // Clear any error messages
        } catch (error) {
          console.error(error);
          this.errorMessage = 'Failed to fetch comments. Please try again later.'; // Handle any errors
        }
      } else {
        this.errorMessage = 'Invalid TikTok link. Please check and try again.'; // Handle invalid TikTok links
      }
    }
  }
};
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 60px;
}

input {
  padding: 10px;
  margin-right: 10px;
}

button {
  padding: 10px;
}
</style>