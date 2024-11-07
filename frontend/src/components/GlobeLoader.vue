<template>
  <div class="popup-wrapper">
    <div class="demo-wrapper">
      <div class="globe-loader fas fa-globe-americas" :style="{ fontSize: size }">
        <i class="fas fa-plane"></i>
      </div>
    </div>
    <!-- Display dynamic loading message -->
    <p class="loading-message">{{ message }}</p>
  </div>
</template>

<script>
import '@fortawesome/fontawesome-free/css/all.css';

export default {
  name: "GlobeLoader",
  props: {
    size: {
      type: String,
      default: "10rem" // Default size
    },
    message: {
      type: String,
      default: "Sending details over..." // Default message if no message is provided
    }
  },
  mounted() {
    console.log("Globe size prop:", this.size); // Log size prop when component mounts
  }
};
</script>

<style scoped>
/* Globe Loader Styles */
.globe-loader {
  --loader-color: #3f94a7; /* Define color variable locally */
  position: relative;
  font-size: 10rem;
  color: var(--loader-color); /* Use the locally defined variable */
  margin: 4rem;
}

.globe-loader > i {
  display: block;
  position: absolute;
  font-size: 0.2em;
  height: 50%;
  top: 0;
  left: 50%;
  transform: translateX(-50%) rotate(0deg);
  transform-origin: center bottom;
  animation: loader-spin 3s infinite ease-in-out;
  color: var(--loader-color); /* Use the color variable for the plane */
  &::before {
      position: relative;
      top:-1.25em;
}
}

/* Keyframe animation for spinning */
@keyframes loader-spin {
  from {
    transform: translateX(-50%) rotate(0deg);
  }
  to {
    transform: translateX(-50%) rotate(360deg);
  }
}

.popup-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  min-width: 200px;
  width: 35%;
  height: 40%
}

.demo-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

.loading-message {
  font-size: 1.2rem;
  color: #3f94a7;
  text-align: center;
}
</style>