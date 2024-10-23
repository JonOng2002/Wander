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
    placeId: {
      type: String,
      required: false,
    },
    placeName: {
      type: String,
      required: true,
    },
    vicinity: {
      type: String,
      required: false,
    },
    country: {
      type: String,
      required: true,
    },
    city: {
      type: String,
      required: true,
    },
    latitude: {
      type: Number,
      required: true,
    },
    longitude: {
      type: Number,
      required: true,
    },
    placePng: {
      type: String,
      required: false,
    },
    userId: {
      type: String,
      required: true,
    },
    activities: {
      type: Array,
      required: true,
    },
    summary: {
      type: String,
      required: false,
    },
    source: {
      type: String,
      required: false,
    },
  },
  methods: {
    async savePlace() {
      const db = getFirestore();

      // Check if userId is valid
      if (!this.userId) {
        console.error("User ID is required to save a place.");
        return;
      }

      const userRef = doc(db, "users", this.userId);

      const placeData = {
        activities: this.activities || [],
        city: this.city || "Unknown city",
        coordinates: {
          latitude: this.latitude,
          longitude: this.longitude,
        },
        country: this.country,
        image: this.placePng,
        name: this.placeName,
        place_id: this.placeId || "saved_places",
        source: this.source || "saved_places",
        summary: this.summary || "No summary available.",
        timestamp: Timestamp.now(),
        vicinity: this.vicinity || "Unknown vicinity",
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
    },
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