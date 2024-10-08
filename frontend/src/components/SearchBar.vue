<template>
    <div class="search-bar d-flex justify-content-center">
      <form @submit.prevent="submitLink" class="d-flex w-100 w-lg-50 w-md-75">
        <input
          type="text"
          v-model="link"
          class="form-control"
          placeholder="Enter a link"
          required
        />
        <button type="submit" class="btn btn-primary btn-lg ms-2">Analyze</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SearchBar',
    data() {
      return {
        link: '', // Data binding for the input field
      };
    },
    methods: {
      submitLink() {
        // Emit the link to the parent component
        this.$emit('submit-link', this.link);
        // Clear the input field after submission
        this.link = '';
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
  