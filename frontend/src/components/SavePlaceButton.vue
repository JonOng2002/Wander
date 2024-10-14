<template>
  <button @click="savePlace">Save Place</button>
</template>

<script setup>
import { getFirestore, collection, addDoc } from 'firebase/firestore';

// Props: `placeName` and `userId`
const props = defineProps({
  placeName: {
    type: String,
    required: true
  },
  userId: {
    type: String,
    required: true
  }
});

// Firestore initialization
const db = getFirestore();

// Function to save the place to Firestore
const savePlace = async () => {
  if (!props.placeName || !props.userId) {
    console.error('Missing placeName or userId');
    return;
  }
  
  try {
    const docRef = await addDoc(collection(db, 'savedPlaces'), {
      placeName: props.placeName,
      userId: props.userId,
      timestamp: new Date(),
    });
    console.log('Place saved with ID: ', docRef.id);
  } catch (e) {
    console.error('Error adding document: ', e);
  }
};
</script>