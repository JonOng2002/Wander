<template>
  <button class="save-button" @click="savePlace">
    Save Place
  </button>
</template>

<script>
import { doc, updateDoc, arrayUnion } from "firebase/firestore";
import { getFirestore, Timestamp } from "firebase/firestore";

export default {
  name: "SavePlaceButton",
  props: {
    placeId: String,
    placeName: String,
    vicinity: String,
    country: String,
    city: String,
    latitude: Number,
    longitude: Number,
    placePng: String,
    userId: String,
    activities: Array,
    summary: String,
    source: String,
  },
  methods: {
    async savePlace() {
  const db = getFirestore();

  // Check if userId is valid
  if (!this.userId) {
    console.error("User ID is required to save a place.");
    return; // Prevent further execution
  }

  const userRef = doc(db, "users", this.userId);

  const placeData = {
    activities: this.activities,
    city: this.city,
    coordinates: {
      latitude: this.latitude,
      longitude: this.longitude,
    },
    country: this.country,
    image: this.placePng,
    name: this.placeName,
    place_id: this.placeId,
    source: this.source,
    summary: this.summary,
    timestamp: Timestamp.now(),
    vicinity: this.vicinity,
  };

  console.log("Saving place data:", placeData);

  if (!placeData.place_id || !placeData.name || !placeData.vicinity) {
    console.error("Attraction not found for saving.", placeData);
    return;
  }

  try {
    console.log("Updating document at:", userRef);
    await updateDoc(userRef, {
      savedPlaces: arrayUnion(placeData),
    });
    this.$emit("place-saved");
  } catch (error) {
    console.error("Error saving place:", error.message || error);
  }
}

,
  },
};
</script>

<style scoped>
.save-button {
  background-color: black;
  color: white;
  padding: 8px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.save-button:hover {
  background-color: #333;
}
</style>
