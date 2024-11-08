<template>
  <div class="modal-overlay" @click.self="cancel">
    <div class="modal-content">
      <slot></slot>
      <div class="modal-buttons">
        <button class="confirm-button" @click="handleYesClick">Yes</button>
        <button class="cancel-button" @click="cancel">No</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineEmits } from 'vue';
import { useRouter } from 'vue-router';

const emit = defineEmits(['confirm', 'cancel']);
const router = useRouter(); // Initialize the router

// Function to handle "Yes" click
const handleYesClick = () => {
  emit('confirm');
  router.push({ name: 'SavedItinerary' }); // Redirect to SavedItinerary.vue
};

const cancel = () => {
  emit('cancel');
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  padding: 30px;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
  text-align: center;
}

.modal-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.confirm-button,
.cancel-button {
  background-color: #3f94a7;
  color: #fff;
  border: none;
  padding: 10px 20px;
  margin: 0 10px;
  border-radius: 5px;
  cursor: pointer;
}

.confirm-button:hover,
.cancel-button:hover {
  background-color: #0056b3;
}

.confirm-button {
  background-color: #dc3545;
}

.confirm-button:hover {
  background-color: #c82333;
}
</style>