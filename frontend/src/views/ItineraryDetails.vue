<template>
    <div class="generated-itinerary">

        <AppNavbar class="sticky-top" v-if="false"></AppNavbar> <!-- Navbar hidden on this page -->

        <div v-if="loading" class="empty-message">Loading itinerary...</div>
        <div v-else-if="!itinerary || !itinerary.itinerary || !itinerary.itinerary.length" class="empty-message">
            <p>No itinerary found.</p>
        </div>

        <div v-else class="main-content">
            <!-- Left Side: Itinerary Details -->
            <div class="itinerary-details-container">
                <div class="itinerary-details">
                    <!-- Close Button to exit the page -->
                    <button class="close-button" @click="closeItinerary">✕</button>
                    <div class="row justify-content-between align-items-center g-0">
                        <div class="col-12 date-column">
                            <p>Review our recommendations</p>
                            <h2>Personalized itinerary for <strong>{{ itinerary.userName || 'Guest' }}</strong></h2>
                            <p>{{ itinerary.country }} • {{ getNumDays() }} days</p>
                        </div>
                        <button @click="deleteItinerary" class="delete-button">Delete Itinerary</button>
                    </div>

                    <div v-for="(places, dayIndex) in splitIntoDays(itinerary.itinerary)" :key="dayIndex"
                        class="day-section">
                        <div class="day-header">Day {{ dayIndex + 1 }}</div>
                        <p class="day-description">
                            Embark on a captivating journey through Japan’s diverse cultural and historical gems.
                            Your adventure begins with a visit to the Cup Noodles Museum Yokohama.
                        </p>
                        <div class="itinerary-table">
                            <div class="itinerary-item" v-for="(place, timeIndex) in places" :key="timeIndex">
                                <div class="time-column">{{ generateTime(timeIndex) }}</div>
                                <div class="place-column">
                                    <img :src="place.image" class="place-image" :alt="place.name" />
                                    <h5>{{ place.name }}</h5>
                                    <p>{{ place.vicinity }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right Side: Google Maps -->
            <div class="map-container">
                <div id="location-map" class="map">
                    <GoogleMap :center="mapCenter" :zoom="15" style="width: 100%; height: 100%">
                        <Marker v-for="place in itinerary.itinerary" :key="place.place_id"
                            :position="{ lat: place.coordinates.latitude, lng: place.coordinates.longitude }" />
                    </GoogleMap>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import { ref, onMounted } from "vue";
import { getFirestore, doc, getDoc, updateDoc } from "firebase/firestore";
import { getAuth } from "firebase/auth";
import { useRoute } from "vue-router";
import { GoogleMap, Marker } from 'vue3-google-map';
import router from "@/router";

export default {
    name: "ItineraryDetails",
    components: {
        GoogleMap,
        Marker,
    },
    setup() {
        const itinerary = ref(null);
        const loading = ref(true);
        const db = getFirestore();
        const route = useRoute();
        const mapCenter = ref({ lat: 35.6762, lng: 139.6503 }); // Default center for Tokyo, Japan
        const timeSlots = ['09:00 AM', '11:00 AM', '02:00 PM', '04:00 PM'];

        // Fetch the itinerary based on the savedAt identifier passed through the route
        onMounted(async () => {
            const savedAt = route.params.savedAt;  // Use the savedAt from the params
            const userId = route.query.userId || getAuth().currentUser.uid;  // Ensure you're getting the correct user ID

            console.log("SavedAt from route params:", savedAt);  // Debugging
            console.log("User ID:", userId);  // Debugging

            if (savedAt !== undefined && userId) {
                const docRef = doc(db, "users", userId);
                const docSnap = await getDoc(docRef);

                if (docSnap.exists()) {
                    const savedItineraries = docSnap.data().savedItineraries || [];

                    console.log("Saved itineraries:", savedItineraries);  // Debugging

                    // Retrieve the correct itinerary based on the savedAt identifier
                    itinerary.value = savedItineraries.find(itin => itin.savedAt === savedAt);

                    console.log("Selected itinerary:", itinerary.value);  // Debugging

                    if (itinerary.value && itinerary.value.itinerary.length > 0) {
                        const firstPlace = itinerary.value.itinerary[0];
                        mapCenter.value = { lat: firstPlace.coordinates.latitude, lng: firstPlace.coordinates.longitude };
                    } else {
                        console.error("Itinerary not found for savedAt:", savedAt);  // Debugging
                    }
                }
            }
            loading.value = false;
        });

        // Delete the itinerary from Firestore when delete button is clicked
        const deleteItinerary = async () => {
            const userId = getAuth().currentUser.uid;
            const savedAt = route.params.savedAt;

            if (userId && savedAt) {
                const docRef = doc(db, "users", userId);
                const docSnap = await getDoc(docRef);

                if (docSnap.exists()) {
                    let savedItineraries = docSnap.data().savedItineraries || [];
                    savedItineraries = savedItineraries.filter(itin => itin.savedAt !== savedAt);

                    // Update Firestore with the new array
                    await updateDoc(docRef, { savedItineraries });

                    // Navigate back to the saved itineraries page
                    router.push({ name: 'SavedItinerary' });
                }
            }
        };

        const closeItinerary = () => {
            router.push({ name: 'SavedItinerary' }); // Adjust this route if needed
        };

        const generateTime = (index) => {
            return timeSlots[index % timeSlots.length];
        };

        const splitIntoDays = (itinerary) => {
            if (!itinerary || itinerary.length === 0) {
                return [];
            }
            const days = [];
            const daySize = 4;
            for (let i = 0; i < itinerary.length; i += daySize) {
                days.push(itinerary.slice(i, i + daySize));
            }
            return days;
        };

        const getNumDays = () => {
            return Math.ceil(itinerary.value?.itinerary?.length / 4) || 0;
        };

        return {
            itinerary,
            loading,
            generateTime,
            splitIntoDays,
            getNumDays,
            mapCenter,
            deleteItinerary,
            closeItinerary
        };
    },
};
</script>




<style scoped>
.delete-button {
    background-color: #6c757d;
    color: white;
    border: none;
    padding: 10px 20px;
    font-size: 1rem;
    cursor: pointer;
    border-radius: 5px;
    margin-top: 20px;
}

.delete-button:hover {
    background-color: #5a6268;
}

.main-content {
    display: flex;
    height: 100vh;
    /* Full viewport height */
}

.itinerary-details-container {
    width: 50%;
    /* Take half the width */
    overflow-y: auto;
    /* Allow scrolling within this section */
    max-height: 100vh;
    /* Limit the height to viewport height */
    padding-right: 10px;
    /* Space for the scrollbar */
}

.itinerary-details {
    padding: 20px;
}

.itinerary-details::-webkit-scrollbar {
    width: 8px;
    /* Narrower scrollbar */
}

.itinerary-details::-webkit-scrollbar-track {
    background: #f1f1f1;
}

.itinerary-details::-webkit-scrollbar-thumb {
    background-color: #888;
    /* Gray scrollbar */
}

.itinerary-details::-webkit-scrollbar-thumb:hover {
    background-color: #555;
    /* Darker on hover */
}

.day-section {
    margin-bottom: 20px;
    background-color: #fdfdfd;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.day-header {
    font-weight: bold;
    font-size: 1.5rem;
    margin-bottom: 10px;
}

.day-description {
    margin-bottom: 20px;
    color: #666;
}

.itinerary-table {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    /* Two items per row */
    gap: 15px;
}

.itinerary-item {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.time-column {
    text-align: left;
    font-weight: bold;
    padding: 10px 0;
}

.place-column {
    padding: 10px 0;
}

.place-column h5 {
    font-size: 1.2rem;
    margin: 0;
}

.place-column img {
    max-width: 150px;
    border-radius: 8px;
}

.map-container {
    background-color: #F8F9FA;
    width: 50%;
    /* Take the other half of the width */
    position: sticky;
    top: 0;
    height: 100vh;
    /* Full viewport height */
    overflow: hidden;
}

.map {
    width: 100%;
    height: 100%;
    pointer-events: none;
    /* Disable interaction with the map */
}

/* Media query for responsiveness */
@media (max-width: 768px) {
    .map-container {
        display: none;
        /* Hide map on small screens */
    }

    .itinerary-details-container {
        width: 100%;
        /* Take full width on small screens */
    }
}
</style>