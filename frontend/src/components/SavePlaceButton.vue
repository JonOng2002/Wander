<template>
  <button @click="savePlace">Save Place</button>
</template>

<script setup>
import { getFirestore, collection, addDoc } from 'firebase/firestore';

// Props: these fields are passed from the parent
// eslint-disable-next-line
const props = defineProps({
  placeName: {
    type: String,
    required: true,
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
    type: [String, Number], // allow both number and string
    required: true,
  },
  longitude: {
    type: [String, Number],
    required: true,
  },
  placePng: {
    type: String,
    default: '', // fallback if no image is provided
  },
  userId: {
    type: String,
    required: true,
  },
  activities: {
    type: Array,
    default: () => [], // default to empty array
  },
  summary: {
    type: String,
    default: '', // default to empty string
  },
});

// Firestore initialization
const db = getFirestore();

// Function to save the place to Firestore
const savePlace = async () => {
  // Ensure none of the required fields are undefined
  if (!props.placeName || !props.country || !props.city || !props.latitude || !props.longitude || !props.userId || !props.summary || !props.activities) {
    console.error('Missing required data to save the place');
    return;
  }

  try {
    const docRef = await addDoc(collection(db, 'savedPlaces'), {
      placeName: props.placeName,
      country: props.country,
      city: props.city,
      coordinates: {
        latitude: props.latitude || 0,  // provide default if needed
        longitude: props.longitude || 0, // provide default if needed
      },
      placePng: props.placePng || '',  // optional field
      userId: props.userId,
      timestamp: new Date(),
      activities: props.activities,
      summary: props.summary,
    });
    console.log('Place saved with ID: ', docRef.id);
  } catch (e) {
    console.error('Error adding document: ', e);
  }
};
</script>

<style scoped>
/* Add styles if needed */
</style>