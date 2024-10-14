<script setup>
import { useCollection } from 'vuefire'
import { collection } from 'firebase/firestore'
import { db } from '@/firebase' // Import the Firestore instance you set up

// Define your Firestore collection reference
const placesRef = collection(db, 'places')

// Use the collection in Vuefire
const { data: places } = useCollection(placesRef) // `places` will be reactive
</script>

<template>
  <div>
    <h2>Places List</h2>
    <ul>
      <!-- Loop through the places data from Firestore -->
      <li v-for="place in places" :key="place.id">{{ place.name }}</li>
    </ul>
  </div>
</template>

<style scoped>
/* Add your styles if needed */
</style>