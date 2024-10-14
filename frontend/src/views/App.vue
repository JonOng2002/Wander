<template>
  <div id="app">
    <nav class="navbar">
      <!-- Common Links -->
      <span>
      <router-link class="nav-link" to="/"> Wander </router-link> |
      <router-link class="nav-link" to="/about"> About </router-link> |
      <router-link class="nav-link" to="/home"> HomePage </router-link> |
      <router-link class="nav-link" to="/savedPlace"> Saved Places |
      </router-link>
      </span>
      <!-- Links visible based on authentication state -->
      <span v-if="isLoggedIn"> 
        <router-link class="nav-link" to="/feed"> Feed </router-link> |
        <button class="signout-btn" @click="handleSignOut"> Logout </button>
      </span>
      <span v-else>
        <router-link class="nav-link" to="/register"> Register </router-link> |
        <router-link class="nav-link" to="/signin"> Sign-in </router-link>
      </span>
    </nav>

    <!-- Loading state while checking authentication -->
    <div v-if="loading" class="loading">
      <p>Loading...</p>
    </div>
    <div v-else class="content">
      <router-view></router-view> <!-- Render the actual content after login -->
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getAuth, onAuthStateChanged, signOut } from 'firebase/auth';

// Reactive state variables
const isLoggedIn = ref(false); // Track if the user is logged in
const loading = ref(true); // Track if the app is still checking auth state

const router = useRouter();
const auth = getAuth(); // Get Firebase Auth instance

// Function to sign out the user
const handleSignOut = () => {
  signOut(auth).then(() => {
    isLoggedIn.value = false;
    router.push("/signin"); // Redirect to login page after signing out
  }).catch((error) => {
    console.error("Error signing out: ", error);
  });
};

// Check authentication state when the component is mounted
  onMounted(() => {
  onAuthStateChanged(auth, (user) => {
    loading.value = false; // Stop loading once Firebase auth state is checked
    isLoggedIn.value = !!user; // Set isLoggedIn to true if user is authenticated
  });
});
</script>

<style scoped>
/* General styles for the app */
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 0;
  text-align: center;
}

/* Styles for the navigation bar */
.navbar {
  background-color: #333;
  padding: 1rem;
  color: white;
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

.nav-link:hover {
  color: #ffcc00;
}

/* Button styles for logout */
.signout-btn {
  background-color: #ff5f5f;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-weight: bold;
}

.signout-btn:hover {
  background-color: #ff3333;
}

/* Loading state */
.loading {
  margin-top: 2rem;
  font-size: 1.2rem;
  color: #666;
}

/* General content area styles */
.content {
  margin-top: 2rem;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 8px;
}
</style>