<template>
  <div class="profile-container">
    <h1>Profile</h1>

    <div v-if="user">
      <h3>Welcome, {{ user.displayName || 'User' }}</h3>
      <p><strong>Email:</strong> {{ user.email }}</p>
      
      <!-- Add more user information here if available -->
      
      <div class="actions">
        <button @click="handleSignOut">Logout</button>
      </div>
    </div>

    <div v-else>
      <p>You must be logged in to view this page.</p>
      <router-link to="/signin">Login</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getAuth, onAuthStateChanged, signOut } from 'firebase/auth';
import { useRouter } from 'vue-router';

// State for user data
const user = ref(null);
const router = useRouter();

// Firebase authentication
const auth = getAuth();

// Fetch user info on component mount
onMounted(() => {
  onAuthStateChanged(auth, (currentUser) => {
    if (currentUser) {
      user.value = currentUser;  // Store the user object in state
    } else {
      console.error("No user is logged in");
      router.push('/signin');  // Redirect to login if not authenticated
    }
  });
});

// Function to log out the user
const handleSignOut = () => {
  signOut(auth).then(() => {
    user.value = null;  // Clear the user data
    router.push('/signin');  // Redirect to login page
  }).catch((error) => {
    console.error("Error signing out: ", error);
  });
};
</script>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

h1 {
  font-size: 2em;
  margin-bottom: 20px;
}

.actions {
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  background-color: red;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #000000;
}
</style>