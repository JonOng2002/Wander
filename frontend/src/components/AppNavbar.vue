<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom-black w-100">
    <div class="container-fluid d-flex justify-content-between align-items-center">
      <!-- Title -->
      <a class="navbar-brand" href="#">
        <h1 id="title" class="h1">wander.</h1>
      </a>

      <!-- Navigation Links -->
      <ul class="navbar-nav d-flex flex-row align-items-center">
        <li class="nav-item me-4">
          <router-link to="/mainpage" class="nav-link">Home</router-link>
        </li>
        <li class="nav-item me-4">
          <router-link to="/itinerary" class="nav-link">Saved Places</router-link>
        </li>
        <li class="nav-item me-4">
          <router-link to="/upload" class="nav-link">Destinations</router-link>
        </li>
        <li class="nav-item me-4">
          <router-link to="/analyze" class="nav-link">Link:</router-link>
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
#title {
  font-family: 'Lobster Two', cursive;
  font-size: 2.5vw;
  color: black;
  margin-left: 20px;
}
.navbar{
  border: 1px solid black
}
.nav-link {
  font-weight: bold;
  font-size: 1.5vw;
  color: black;
  font-family: 'Cormorant Garamond', serif;
}

.nav-link:hover {
  text-decoration: underline;
}

.profile-pic {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
</style>
