<template>
  <div class="profile-page">
    <h1>Welcome to the Profile Page</h1>
    <p>This is your profile page content.</p>

    <button @click="logout" class="btn btn-danger">Logout</button>
  </div>
</template>

<script>
export default {
  name: 'ProfilePage',
  methods: {
    logout() {
      // Clear user session data here (if applicable)
      // For example: localStorage.removeItem('userToken');

      // Route to the sign-in page after logging out
      this.$router.push({ name: 'SignIn' });
    },
  },
};
</script>

<style scoped>
.profile-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 20px;
}

p {
  font-size: 1.2rem;
  margin-bottom: 40px;
}

button {
  font-size: 1rem;
  padding: 10px 20px;
}
</style>
