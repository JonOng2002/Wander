<template>
  <nav class="navbar navbar-expand-lg sticky-top w-100">
    <div class="nav-contain container-fluid d-flex justify-content-between align-items-center">
      <!-- Title -->
      <router-link to="/about" class="navbar-brand nav-link">
  <h1 id="title">wander.</h1>
</router-link>

      <!-- Navigation Links (hidden below md breakpoint) -->
      <ul v-if="!isMobile" class="navbar-nav d-flex flex-row align-items-center ms-auto">
        <li class="nav-item me-4">
          <router-link to="/" class="nav-link" exact>Explore</router-link>
        </li>
        <li class="nav-item me-4">
          <router-link to="/savedplaces" class="nav-link">Saved Places</router-link>
        </li>
        <li class="nav-item me-4">
          <router-link to="/destinations" class="nav-link">Destinations</router-link>
        </li>
        <li class="nav-item me-4">
          <router-link to="/itineraryBuilder" class="nav-link">Itinerary Builder</router-link>
        </li>
        <!-- <li class="nav-item me-4">
          <router-link to="/myitinerary" class="nav-link">middle itinerary</router-link>
        </li> -->
        <li class="nav-item me-4">
          <router-link to="/saveditinerary" class="nav-link">My Itineraries</router-link>
        </li>
      </ul>



      <!-- Profile icon remains on all screen sizes -->
      <!-- Profile Picture and Dropdown Button -->
      <div class="d-flex align-items-center">
        <!-- Dropdown Button (Visible below md breakpoint) -->
        <button v-if="isMobile" @click="toggleDropdownMenu" class="dropdown-btn">
          ☰
        </button>

        <img src="@/assets/profilepic.png" class="user-pic" alt="user-pic" @click="toggleProfileMenu" />

        <div class="sub-menu-wrap" :class="{ 'open-menu': isMenuOpen }" id="subMenu">
          <div class="sub-menu">
            <div class="user-info">
              <img src="@/assets/profilepic.png" />
              <h3>{{ displayName || "User" }}</h3>

              <div class="user-email">
                <h4>{{ email }}</h4>
              </div>
            </div>

            <hr />


            <a href="#" class="sub-menu-link" @click="signOutUser">
              <img src="@\assets\logout_icon.png" alt="" />
              <p>Logout</p>
              <span>></span>
            </a>
          </div>
        </div>
      </div>

      <!-- Overlay when dropdown is open -->
      <div v-if="isDropdownOpen" class="overlay" @click="closeDropdown"></div>

      <!-- Dropdown Menu (Only visible when dropdown button is clicked) -->
      <div class="mobile-dropdown-wrap" :class="{ 'open-menu': isDropdownOpen }">
        <div class="mobile-dropdown">
          <router-link to="/" class="dropdown-item" exact>Explore</router-link>
          <router-link to="/savedplaces" class="dropdown-item">Saved Places</router-link>
          <router-link to="/destinations" class="dropdown-item">Destinations</router-link>
          <router-link to="/itineraryBuilder" class="dropdown-item">Build Itinerary</router-link>
          <router-link to="/saveditinerary" class="dropdown-item">My itineraries</router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { getAuth, onAuthStateChanged, signOut } from "firebase/auth";

export default {
  name: "AppNavbar",
  data() {
    return {
      isMenuOpen: false, // Initialize the menu state
      isDropdownOpen: false, // Mobile dropdown menu state
      isMobile: false,
      displayName: "", // Initialize the display name
      email: "", // Initialize the email
    };
  },
  methods: {
    toggleProfileMenu() {
      this.isMenuOpen = !this.isMenuOpen; // Toggle the menu state
    },

    toggleDropdownMenu() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },

    closeDropdown() {
      this.isDropdownOpen = false;
    },


    checkScreenWidth() {
      this.isMobile = window.innerWidth < 768; // Adjust based on the md breakpoint
    },

    fetchUserData(user) {
      if (user) {
        this.displayName = user.displayName || "User"; // Set the display name or fallback to 'User'
        this.email = user.email; // Set the email
      }
    },

    async signOutUser() {
      const auth = getAuth();
      try {
        await signOut(auth);
        console.log("User signed out");
        this.displayName = ""; // Clear the display name
        this.email = ""; // Clear the email
        this.$router.push("/login"); // Redirect to the main page
      } catch (error) {
        console.error("Error signing out:", error);
      }
    },
  },

  watch: {
    $route() {
      this.isDropdownOpen = false; // Automatically close dropdown on route change
    }
  },

  mounted() {
    this.checkScreenWidth();
    window.addEventListener("resize", this.checkScreenWidth);

    //Fetch user data on component mount
    const auth = getAuth();

    onAuthStateChanged(auth, (user) => {
      if (user) {
        // User is signed in, set the username and email
        this.fetchUserData(user);
      } else {
        // User is signed out, handle accordingly
        console.log("No user is signed in");
      }
    });
  },

  beforeUnmount() {
    window.removeEventListener("resize", this.checkScreenWidth);
  },
};
</script>

<style scoped>
/* Sticky navbar */
.navbar {
  background-color: #3f94a7;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  /* Subtle shadow for depth */
  padding: 15px 20px;
  /* Add padding for better spacing */
  z-index: 1000;
  /* Ensure navbar stays on top of other elements */
}

/* Navbar title styling */
#title {
  font-family: "Lobster Two", cursive;
  font-size: 2.5vw;
  color: white;
  margin-left: 20px;
  min-width: 80px;
  /* Set a minimum width to prevent shrinking */
}

/* Container background */
.nav-contain {
  background-color: #3f94a7;
}

/* Navigation link styling */
.nav-link {
  font-weight: 400;
  font-size: 1.5vw;
  color: white !important;
  /* Ensure links stay white */
  position: relative;
  font-family: "Source Sans 3", sans-serif;
  /* Position for sliding background */
  padding: 5px 10px;
  /* Add padding for better click area */
  border-radius: 100px;
  /* Rounded corners for links */
}

/* Hover state for links */
.nav-link:hover {
  color: #ffffff !important;
  /* Soft hover effect */
  background-color: rgba(255, 255, 255, 0.4);
  /* Semi-transparent background */
  border: 1px solid white;
  /* Add border on hover */
}

/* Sliding background effect using the before pseudo-element */
.router-link::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: white;
  z-index: -1;
  /* Keep the background behind the text */
  border-radius: 100px;
  /* Match border radius with links */
}

.router-link:active,
.router-link-exact-active {
  color: #ffffff !important;
  /* Soft hover effect */
  background-color: rgba(255, 255, 255, 0.4);
  /* Semi-transparent background */
  border: 1px solid white;
}

/* Profile picture styling */
.profile-pic {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid white;
  /* Add a border to make it more visible */
}

/* Sticky positioning */
.sticky-top {
  top: 0;
  position: sticky;
  z-index: 1020;
  /* Higher z-index to ensure navbar stays above other elements */
  background-color: #3f94a7;
  /* Ensure the background remains black */
}

/*====== MOBILE(small) VIEW ======*/

/* Hide mobile dropdown by default */
.mobile-nav {
  display: none;
}

/* Dropdown Button (only visible on mobile) */
.dropdown-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: white;
  cursor: pointer;
  margin-right: 10px;
}

/* Overlay when dropdown is open */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  /* Translucent black filter */
  z-index: 1040;
  /* Behind the navbar and dropdown */
}

.mobile-dropdown-wrap {
  position: absolute;
  top: 100%;
  right: 0;
  width: 100%;
  max-height: 0;
  overflow: hidden;
  transition: max-height 1.2s ease;
  /* Smooth expand/collapse animation */
  z-index: 1050;
}

.mobile-dropdown-wrap.open-menu {
  max-height: 100vh;
  /* Adjust to fit the number of items */
}

.mobile-dropdown {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  padding: 10px 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 15px;
  font-size: 1rem;
  color: #333;
  text-decoration: none;
  border-bottom: 1px solid #e0e0e0;
  transition: transform 0.3s ease;
}

.dropdown-item:last-child {
  border-bottom: none;
}

/* Active page color */
.dropdown-item.router-link-exact-active {
  color: #a8a8a8 !important;
  /* Set active page color to gray */
  font-weight: 600;
}

.dropdown-item:hover {
  background-color: #0057d9;
  transform: scale(1.05);
  /* Slightly scale up the card */
}

/*====== USER PROFILE MENU ======*/
.user-pic {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-left: 30px;
  cursor: pointer;
  background-color: white;
}

.sub-menu-wrap {
  position: absolute;
  top: 100%;
  right: 1%;
  width: 320px;
  max-height: 0px;
  overflow: hidden;
  transition: max-height 0.6s;
  z-index: 1050;
}

.sub-menu-wrap.open-menu {
  max-height: 400px;
}

.sub-menu {
  background: #fff;
  padding: 0px;
  margin: 8px;
  border-radius: 5%;
  overflow: hidden;
  z-index: 1050;
}

.user-info {
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
  text-align: center;
  width: 100%;
  overflow: hidden;
  background-color: #f0f6ff;
  padding: 1rem;
  z-index: 1050;
}

.user-info h3 {
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
  font-size: 1.2rem;
  margin: 0;
  display: block;
  z-index: 1050;
}

.user-email {
  font-weight: 300;
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.user-email h4 {
  font-weight: 300;
  font-size: 0.9rem;
  margin: 0;
  display: block;
  /* Ensure block-level behavior */
  white-space: nowrap;
  /* Prevent text from wrapping */
  overflow: hidden;
  /* Hide overflowed text */
  text-overflow: ellipsis;
  /* Add ellipsis (...) */
  max-width: 100%;
  /* Ensure ellipsis works within available space */
}

.user-info img {
  width: 60px;
  height: 60px;
  border-radius: 50%;
}

.sub-menu hr {
  height: 1px;
  border: 0;
  width: 100%;
  background: #ccc;
  margin: 0;
}

.sub-menu-link {
  display: flex;
  align-items: center;
  margin: 10px 0;
  padding: 0px 1.5rem;
  text-decoration: none;
  color: #333;
  background-color: white;
}

.sub-menu-link:last-child {
  margin-bottom: 1rem;
}

.sub-menu-link p {
  flex: 1;
  margin: 0;
}

.sub-menu-link img {
  width: 40px;
  height: 40px;
  background: #e5e5e5;
  margin-right: 15px;
  border-radius: 50%;
  padding: 8px;
}

.sub-menu-link span {
  font-size: 22px;
  transition: transform 0.3s;
}

.sub-menu-link:hover span {
  transform: translateX(5px);
}

.sub-menu-link:hover p {
  font-weight: 600;
}

/* ****************responsive styles*************** */
/* Responsive Styles */
@media (max-width: 768px) {

  .navbar-nav {
    display: none;
  }

  /* Show the dropdown button and mobile nav only on small screens */
  .navbar-toggler {
    display: inline;
    background: none;
    border: none;
    color: white;
    font-size: 24px;
  }

  /* Hide desktop navigation links */
  .desktop-nav {
    display: none;
  }

  /* Display mobile nav when toggled */
  .mobile-nav {
    display: block;
    position: absolute;
    top: 60px;
    left: 0;
    width: 100%;
    background-color: #0057d9;
    z-index: 1000;
  }

  .mobile-nav .nav-link {
    display: block;
    padding: 10px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.3);
  }

  #title {
    font-size: 1.2rem;
    /* Set a fixed size to maintain consistency on small screens */
  }
}

/* Additional styles for very small screens (below 320px) */
@media (max-width: 320px) {

  /* Hide the wander logo and profile picture */
  .navbar-brand,
  .user-pic {
    display: none;
  }

  /* Keep the dropdown button visible */
  .dropdown-btn {
    display: inline-block;
    margin-left: auto;
    /* Align dropdown button to the right */
  }
}
/* Ensure the parent container doesn't wrap */


/* Adjust the profile picture size between 768px and 815px */
@media (max-width: 992px) and (min-width: 768px) {
  .user-pic {
    width: 1.5rem;
    height: 1.5rem;
    margin-left: 1rem;
  }

  .nav-contain {
    justify-content: space-between;
  }
}

</style>
