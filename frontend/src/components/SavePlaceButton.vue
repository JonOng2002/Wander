<template>
  <button @click="savePlace">Save Place</button>
</template>

<script setup>
import { getFirestore, collection, addDoc, doc, updateDoc, arrayUnion } from 'firebase/firestore';
import { defineProps } from 'vue';

// Props: these fields are passed from the parent
const props = defineProps({
  placeId: {
    type: String,
    default: () => `manual-${Date.now()}`,
  },
  placeName: {
    type: String,
    required: true,
  },
  vicinity: {
    type: String,
    default: '', // Use vicinity or city
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
  source: {
    type: String,
    default: 'manual_entry', // Can be 'google_places' or 'manual_entry'
  }
});

// Firestore initialization
const db = getFirestore();

// Function to save the place to the user's savedPlaces collection
const savePlace = async () => { // Inside `savePlace` in save-place-button.vue
  // Check for undefined fields
  if (!props.placeId || !props.placeName || !props.country || !props.city || !props.latitude || !props.longitude || !props.userId) {
    console.error('Missing required data to save the place', {
      placeId: props.placeId,
      placeName: props.placeName,
      country: props.country,
      city: props.city,
      latitude: props.latitude,
      longitude: props.longitude,
      userId: props.userId,
    });
    return;
  }

  try {
    // Create a new document in the 'savedPlaces' collection
    const docRef = await addDoc(collection(db, 'savedPlaces'), {
      place_id: props.placeId,
      name: props.placeName,
      vicinity: props.vicinity || props.city,
      country: props.country,
      city: props.city,
      coordinates: {
        latitude: props.latitude || 0,
        longitude: props.longitude || 0,
      },
      image: props.placePng || '',  // optional field
      activities: props.activities || [], // optional array
      summary: props.summary || '', // optional summary
      source: props.source, // distinguish between 'google_places' or 'manual_entry'
      userId: props.userId,
      timestamp: new Date(),
    });

    console.log('Place saved with ID: ', docRef.id);

    // Add the place reference to the user's 'savedPlaces' field in 'users' collection
    const userRef = doc(db, 'users', props.userId);
    await updateDoc(userRef, {
      savedPlaces: arrayUnion({
        place_id: props.placeId,
        name: props.placeName,
        vicinity: props.vicinity || props.city,
        country: props.country,
        city: props.city,
        coordinates: {
          latitude: props.latitude || 0,
          longitude: props.longitude || 0,
        },
        image: props.placePng || '',  // optional field
        activities: props.activities || [], // optional array
        summary: props.summary || '', // optional summary
        source: props.source,
        timestamp: new Date(),
      })
    });

    console.log('Place added to user\'s savedPlaces list.');

  } catch (e) {
    console.error('Error adding document: ', e);
  }
};
</script>

<style scoped>
/* Add any relevant styles */
</style>