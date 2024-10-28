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
          <router-link to="/myitineraries" class="nav-link">My itineraries</router-link>
        </li>
        <li class="nav-item me-4">
          <router-link to="/generateditinerary" class="nav-link">Generated Itineraries</router-link>
        </li>

        <li>
          <img src="@/assets/profilepic.png" class="user-pic" alt="user-pic" @click="toggleMenu" />

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

              <a href="#" class="sub-menu-link">
                <img
                  src="https://png.pngtree.com/png-vector/20210604/ourmid/pngtree-gray-network-placeholder-png-image_3416659.jpg"
                  alt="" />
                <p>Edit Profile</p>
                <span>></span>
              </a>

              <a href="#" class="sub-menu-link">
                <img
                  src="https://png.pngtree.com/png-vector/20210604/ourmid/pngtree-gray-network-placeholder-png-image_3416659.jpg"
                  alt="" />
                <p>Settings</p>
                <span>></span>
              </a>

              <a href="#" class="sub-menu-link">
                <img
                  src="https://png.pngtree.com/png-vector/20210604/ourmid/pngtree-gray-network-placeholder-png-image_3416659.jpg"
                  alt="" />
                <p>Help</p>
                <span>></span>
              </a>

              <a href="#" class="sub-menu-link" @click="signOutUser">
                <img
                  src="https://png.pngtree.com/png-vector/20210604/ourmid/pngtree-gray-network-placeholder-png-image_3416659.jpg"
                  alt="" />
                <p>Logout</p>
                <span>></span>
              </a>
            </div>
          </div>
        </li>
      </ul>
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
      displayName: "", // Initialize the display name
      email: "", // Initialize the email
    };
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen; // Toggle the menu state
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

  mounted() {
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
};
</script>

<style scoped>
/* Sticky navbar */
.navbar {
  background-color: #0057d9;
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
}

/* Container background */
.nav-contain {
  background-color: #0057d9;
}

/* Navigation link styling */
.nav-link {
  font-weight: bold;
  font-size: 1.5vw;
  color: white !important;
  /* Ensure links stay white */
  font-family: "Cormorant Garamond", serif;
  position: relative;
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

.router-link:active, .router-link-exact-active {
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
  background-color: #0057d9;
  /* Ensure the background remains black */
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
  font-family: "Poppins", serif;
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
</style>
