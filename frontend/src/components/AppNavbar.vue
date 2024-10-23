<template>
  <nav class="navbar navbar-expand-lg sticky-top w-100">
    <div class="nav-contain container-fluid d-flex justify-content-between align-items-center">
      <!-- Title -->
      <a class="navbar-brand" href="#">
        <h1 id="title" class="h1">wander.</h1>
      </a>

      <!-- Navigation Links -->
      <ul class="navbar-nav d-flex flex-row align-items-center">
        <li class="nav-item me-4">
          <router-link to="/" class="nav-link">Main Page</router-link>
        </li>
        <li class="nav-item me-4">
          <router-link to="/savedplaces" class="nav-link">Saved Places</router-link>
        </li>
        <li class="nav-item me-4">
          <router-link to="/destinations" class="nav-link">Destinations</router-link>
        </li>
        <li class="nav-item me-4">
          <router-link to="/about" class="nav-link">About</router-link>
        </li>
        <li class="nav-item me-4">
          <router-link to="/myitinerary" class="nav-link">middle itinerary</router-link>
        </li>
        <li class="nav-item me-4">
          <router-link to="/saveditinerary" class="nav-link">My itineraries</router-link>
        </li>
        <!-- Profile Picture -->
        <li class="nav-item me-4">
          <router-link to="/profile" class="nav-link">
            <img src="@/assets/profilepic.png" alt="Profile" class="profile-pic img-fluid">
          </router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'AppNavbar',
};
</script>

<style scoped>
/* Sticky navbar */
.navbar {
  background-color: black;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
  padding: 15px 20px; /* Add padding for better spacing */
  z-index: 1000; /* Ensure navbar stays on top of other elements */
}

/* Navbar title styling */
#title {
  font-family: 'Lobster Two', cursive;
  font-size: 2.5vw;
  color: white;
  margin-left: 20px;
}

/* Container background */
.nav-contain {
  background-color: black;
}

/* Navigation link styling */
.nav-link {
  font-weight: bold;
  font-size: 1.5vw;
  color: white !important; /* Ensure links stay white */
  font-family: 'Cormorant Garamond', serif;
  transition: color 0.3s ease;
}

.nav-link:hover {
  text-decoration: underline;
  color: #ffffff !important; /* Soft hover effect */
}

/* Active link styling */
.router-link-active,
.router-link-exact-active {
  color: white !important; /* Ensure active links stay white */
  text-decoration: underline;
}

/* Profile picture styling */
.profile-pic {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid white; /* Add a border to make it more visible */
}

/* Sticky positioning */
.sticky-top {
  top: 0;
  position: sticky;
  z-index: 1020; /* Higher z-index to ensure navbar stays above other elements */
  background-color: black; /* Ensure the background remains black */
}
</style>
