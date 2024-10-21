<template>
    <div>
        <h2>Your Itinerary</h2>
        <ul v-if="itinerary.length > 0">
            <li v-for="(place) in itinerary" :key="place.place_id">
                {{ place.name }} - {{ place.vicinity }}
                <button @click="removePlace(place.place_id)">Remove</button>
            </li>
        </ul>
        <div v-else>
            <p>No places in itinerary.</p>
        </div>

        <button @click="clearItinerary">Clear Itinerary</button>
        <button @click="goToCalendarPage">Generate Itinerary</button>
    </div>
</template>

<script>
import { inject } from 'vue';
import { useRouter } from 'vue-router';
import { getAuth } from 'firebase/auth';

export default {
    name: 'DropdownListBeforeItinerary',
    setup() {
        const itineraryState = inject('itineraryState'); // Inject the global itinerary state
        const router = useRouter();
        const auth = getAuth();
        const userId = auth.currentUser?.uid || null; // Fetch user ID dynamically

        if (!itineraryState) {
            console.error('itineraryState is not provided.');
            return;
        }

        // Method to remove a place from itinerary
        const removePlace = (placeId) => {
            const index = itineraryState.itinerary.findIndex(place => place.place_id === placeId);
            if (index !== -1) {
                itineraryState.itinerary.splice(index, 1);  // This will trigger reactivity
            }
        };

        // Method to clear the entire itinerary
        const clearItinerary = async () => {
            if (userId) {
                await itineraryState.clearItinerary(userId);
                itineraryState.itinerary = []; // Reset locally after clearing
            } else {
                console.error('User is not authenticated.');
            }
        };

        // Method to navigate to calendar page
        const goToCalendarPage = () => {
            const normalizedItinerary = itineraryState.itinerary.map((place) => ({
                place_id: place.place_id || 'unknown',
                name: place.name || 'No Name Provided',
                city: place.city || 'Unknown City',
                country: place.country || 'Unknown Country',
                image: place.image || 'default-image-url.jpg',
                summary: place.summary || 'No description available',
                activities: place.activities || [],
                timestamp: place.timestamp || new Date().toISOString(),
            }));

            router.push({
                name: 'CalendarPage',
                query: {
                    itinerary: JSON.stringify(normalizedItinerary)
                }
            });
        };

        return {
            itinerary: itineraryState.itinerary,
            removePlace,
            clearItinerary,
            goToCalendarPage,
        };
    },
};
</script>

<style scoped>
h2 {
    margin-bottom: 20px;
    font-size: 24px;
    text-align: center;
}

ul {
    list-style-type: none;
    padding: 0;
}

li {
    margin-bottom: 10px;
    font-size: 18px;
}

button {
    margin-left: 10px;
    padding: 5px 10px;
    font-size: 14px;
}

button:hover {
    background-color: #ddd;
    cursor: pointer;
}

p {
    font-size: 18px;
    color: grey;
    text-align: center;
}
</style>