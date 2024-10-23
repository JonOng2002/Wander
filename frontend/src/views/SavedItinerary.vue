<template>
<div class="saved-itineraries-container">
    <h1 class="page-title">Saved Itineraries</h1>

    <div v-if="!savedItineraries.length" class="no-itineraries-message">
    <p>No saved itineraries yet. Start creating your itinerary!</p>
    </div>

    <!-- Cards for saved itineraries -->
    <div v-else class="itineraries-list">
    <div v-for="(itinerary, index) in savedItineraries" :key="index" class="itinerary-card">
        <div class="card shadow-sm">
        <!-- Country Title -->
        <img :src="itinerary.image" class="card-img-top" alt="itinerary country image" />
        <div class="card-body">
            <h5 class="card-title">{{ itinerary.country }}</h5>

            <!-- Short description -->
            <p class="card-text">
            {{ itinerary.numDays }}d{{ itinerary.numDays - 1 }}n trip in {{ itinerary.country }}.
            </p>

            <p class="card-subtext">
            Saved on {{ new Date(itinerary.savedAt).toLocaleDateString() }}
            </p>

            <!-- Button to expand and view full itinerary -->
            <button @click="toggleDetails(index)" class="btn btn-outline-primary">
            {{ itinerary.isExpanded ? "Hide Details" : "View Itinerary" }}
            </button>
        </div>

        <!-- Itinerary details (expanded view) -->
        <div v-if="itinerary.isExpanded" class="itinerary-details">
            <div v-for="(day, dayIndex) in itinerary.days" :key="dayIndex">
            <h6>Day {{ dayIndex + 1 }}</h6>
            <ul>
                <li v-for="(place, placeIndex) in day.places" :key="placeIndex">{{ place.name }}</li>
            </ul>
            </div>
        </div>
        </div>
    </div>
    </div>
</div>
</template>

<script>
import { ref } from "vue";
import { getFirestore, doc, getDoc, setDoc } from "firebase/firestore";
import { getAuth } from "firebase/auth";
import { onMounted } from "vue"; // Ensure computed is imported

export default {
    name: "SavedItinerary",
    setup() {
        const savedItineraries = ref([]);
        const loading = ref(true);
        const db = getFirestore();

        // Fetch data from Firestore
        onMounted(async () => {
        loading.value = true;
        const auth = getAuth();
        const user = auth.currentUser;

        if (user) {
            const userId = user.uid;
            const userRef = doc(db, "users", userId);

            try {
            const userDoc = await getDoc(userRef);
            if (userDoc.exists()) {
                savedItineraries.value = userDoc.data().savedItineraries || [];
                console.log("Saved Itineraries:", savedItineraries.value);
            } else {
                await setDoc(userRef, { savedItineraries: [] });
            }
            } catch (error) {
                console.error("Error getting savedItineraries:", error);
            } finally {
                loading.value = false;
            }
        } else {
            console.error("User is not authenticated");
            loading.value = false;
            }
        });

        const viewItinerary = (itinerary) => {
            // For now, simply log the selected itinerary
            console.log("Selected Itinerary:", itinerary);
        };

        return {
            savedItineraries,
            loading,
            viewItinerary,
        };
    },
};


</script>

<style scoped>
.saved-itineraries-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.page-title {
    font-size: 2.5rem;
    margin-bottom: 30px;
    text-align: center;
}

.no-itineraries-message {
    text-align: center;
    font-size: 1.5rem;
}

.itineraries-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

.itinerary-card {
    display: flex;
    flex-direction: column;
}

.card {
    border-radius: 10px;
    overflow: hidden;
}

.card-title {
    font-size: 1.5rem;
    font-weight: bold;
}

.card-text {
    color: #666;
}

.card-subtext {
    font-size: 0.85rem;
    color: #999;
}

.itinerary-details {
    padding: 15px;
    background-color: #f8f9fa;
}

.itinerary-details h6 {
    font-weight: bold;
    margin-top: 10px;
}

.itinerary-details ul {
    padding-left: 20px;
}

.itinerary-details ul li {
    list-style-type: circle;
}
</style>

