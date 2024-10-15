<template>
    <div class="search-bar d-flex justify-content-center">
      <form @submit.prevent="submitLink" class="d-flex w-100 w-lg-50 w-md-75">
        <input
          type="text"
          v-model="link"
          class="form-control"
          placeholder="Paste TikTok link here!"
          required
          :disabled="isLoading"
        />
        <button type="submit" class="btn btn-primary btn-lg ms-2">Search!</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SearchBar',
    props: {
  tiktokLink: { // New prop for link
    type: String,
    default: ''
  }
},
data() {
  return {
    link: this.tiktokLink, // Bind prop value to local data
  };
},
watch: {
  tiktokLink(newValue) {
    this.link = newValue; // Watch for changes to prop and update local data
  }
},
methods: {
  submitLink() {
    // Emit the link to the parent component
    this.$emit('submit-link', this.link);
  },
},
};
  </script>
  
  <style scoped>
  .search-bar {
    margin-top: 20px;
    padding: 20px;
    height: 6vh; /* Set the height of the search bar */
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: "Roboto", sans-serif;
  }

  .btn {
    background-color: black;
  }

 
  </style>
  