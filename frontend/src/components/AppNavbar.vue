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
          <router-link to="/" class="nav-link" exact>Main Page</router-link>
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
          <router-link to="/itinerary" class="nav-link">My itineraries</router-link>
        </li>
        <li class="nav-item me-4">
          <router-link to="/worldmap" class="nav-link">World Map</router-link>
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

/* Main link when active or hovered */
.router-link-active, .router-link-exact-active, .router-link:hover, .router-link-exact-active:hover {
  position: relative;
  color: black !important; /* Text remains black when active or hovered */
  font-weight: bolder;
  text-decoration: underline; /* No underline */
  padding: 5px 10px; /* Add padding to create space for the background */
  transition: color 0.2s ease-in-out; /* Adjust text color transition timing */
  z-index: 1; /* Text stays above the background */
}

/* Sliding background effect using the before pseudo-element */
.router-link-active::before, .router-link-exact-active::before,
.router-link:hover::before, .router-link-exact-active:hover::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: white; /* White background color */
  transition: transform 0.4s ease-in-out, background-color 0s; /* Smooth sliding effect */
  transform: scaleX(0); /* Initially hidden background */
  transform-origin: left; /* Sliding starts from the left */
  z-index: -1; /* Keep the background behind the text */
  border-radius: 0; /* Apply the same border-radius to the background */
}

/* Trigger the sliding effect on hover or active state */
.router-link-active::before, .router-link-exact-active::before,
.router-link:hover::before, .router-link-exact-active:hover::before {
  transform: scaleX(1); /* Expand background to full width */
  transition: transform 0.4s ease-in-out; /* Ensure the background fills smoothly */
}

/* Ensure the text remains on top of the sliding background */
.router-link, .router-link-active {
  transition: color 0.2s ease-in-out; /* Instant text color change */
}

/* Ensure text color remains black while hovering inside the white background */
.router-link:hover, .router-link-exact-active:hover {
  color: black; /* Keep text black during hover */
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
