<template>
    <div>
      <h2>Upload a Video</h2>
      <form @submit.prevent="handleUpload">
        <input type="file" @change="onFileChange" accept="video/*" />
        <button type="submit">Upload Video</button>
      </form>
      <router-link to="/" style="font-size: 20px; text-decoration: none; color: blue;">
      Go to Home Page
      </router-link>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        videoFile: null,
      };
    },
    methods: {
      onFileChange(event) {
        this.videoFile = event.target.files[0];
      },
      handleUpload() {
        const formData = new FormData();
        formData.append('file', this.videoFile);
  
        // Call the backend API to upload and process the video
        fetch('/api/upload-video', {
          method: 'POST',
          body: formData,
        })
        .then(response => response.json())
        .then(data => {
          console.log(data);
        })
        .catch(error => {
          console.error('Error:', error);
        });
      },
    },
  };
  </script>