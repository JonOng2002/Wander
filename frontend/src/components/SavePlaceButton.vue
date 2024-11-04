<!-- src/components/SavePlaceButton.vue -->
<template>
  <button
    :disabled="isAlreadySaved || isSaving"
    class="save-button"
    @click="handleSave"
  >
    <span v-if="isSaving">Saving...</span>
    <span v-else-if="isAlreadySaved">Saved</span>
    <span v-else>Add to Saved Places</span>
  </button>
</template>

<script>
export default {
  name: "SavePlaceButton",
  props: {
    placeId: { type: String, required: true },
    isAlreadySaved: { type: Boolean, required: true },
  },
  data() {
    return {
      isSaving: false,
    };
  },
  methods: {
    handleSave() {
      if (this.isAlreadySaved || this.isSaving) return;
      this.isSaving = true;
      // Emit the 'save-place' event with the placeId
      this.$emit("save-place", this.placeId);
      // Reset the saving state after a short delay
      setTimeout(() => {
        this.isSaving = false;
      }, 1000); // Adjust the delay as needed
    },
  },
};
</script>

<style scoped>
.save-button {
  margin-top: auto;
  background-color: black;
  color: white;
  padding: 8px;
  font-size: 0.8rem;
  font-weight: bold;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.save-button:hover {
  background-color: #333;
  color: white;
}

.save-button:disabled {
  background-color: gray;
  cursor: not-allowed;
}
</style>
