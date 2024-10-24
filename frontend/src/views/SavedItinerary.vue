<template>
    <div class="saved-itineraries-container">
        <h1 class="page-title">Saved Itineraries</h1>

        <div v-if="!savedItineraries.length" class="no-itineraries-message">
            <p>No saved itineraries yet. Start creating your itinerary!</p>
        </div>

        <!-- Cards for saved itineraries -->
        <div v-else class="itineraries-list">
            <!-- The most recent itinerary card -->
            <div v-if="savedItineraries.length" class="itinerary-card itinerary-card-large">
                <div class="card shadow-sm">
                    <img :src="savedItineraries[0].image" class="card-img-top" alt="itinerary country image" />
                    <div class="card-body">
                        <h5 class="card-title">{{ savedItineraries[0].country }}</h5>
                        <p class="card-text">
                            {{ savedItineraries[0].numDays }}d{{ savedItineraries[0].numDays - 1 }}n trip in {{
                            savedItineraries[0].country }}.
                        </p>
                        <p class="card-subtext">
                            Saved on {{ new Date(savedItineraries[0].savedAt).toLocaleDateString() }}
                        </p>
                        <button @click="toggleDetails(0)" class="btn btn-outline-primary">
                            {{ savedItineraries[0].isExpanded ? "Hide Details" : "View Itinerary" }}
                        </button>
                    </div>
                    <!-- Itinerary details (expanded view) -->
                    <div v-if="savedItineraries[0].isExpanded" class="itinerary-details">
                        <div v-for="(day, dayIndex) in savedItineraries[0].days" :key="dayIndex">
                            <h6>Day {{ dayIndex + 1 }}</h6>
                            <ul>
                                <li v-for="(place, placeIndex) in day.places" :key="placeIndex">{{ place.name }}</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            <!-- The rest of the saved itineraries -->
            <div class="itinerary-cards">
                <div v-for="(itinerary, index) in savedItineraries.slice(1)" :key="index + 1" class="itinerary-card">
                    <div class="card shadow-sm">
                        <img :src="itinerary.image" class="card-img-top" alt="itinerary country image" />
                        <div class="card-body">
                            <h5 class="card-title">{{ itinerary.country }}</h5>
                            <p class="card-text">
                                {{ itinerary.numDays }}d{{ itinerary.numDays - 1 }}n trip in {{ itinerary.country }}.
                            </p>
                            <p class="card-subtext">
                                Saved on {{ new Date(itinerary.savedAt).toLocaleDateString() }}
                            </p>
                            <button @click="toggleDetails(index + 1)" class="btn btn-outline-primary">
                                {{ itinerary.isExpanded ? "Hide Details" : "View Itinerary" }}
                            </button>
                        </div>
                        <!-- Itinerary details (expanded view) -->
                        <div v-if="itinerary.isExpanded" class="itinerary-details">
                            <div v-for="(day, dayIndex) in itinerary.days" :key="dayIndex">
                                <h6>Day {{ dayIndex + 1 }}</h6>
                                <ul>
                                    <li v-for="(place, placeIndex) in day.places" :key="placeIndex">{{ place.name }}
                                    </li>
                                </ul>
                            </div>
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
    width: 100%;
    padding: 20px;
}

.page-title {
    text-align: center;
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.5rem;
    margin-bottom: 40px;
}

.itineraries-list {
    display: flex;
    flex-direction: column;
    gap: 30px;
}

.itinerary-card {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s ease;
}

.itinerary-card:hover {
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.itinerary-card-large {
    display: block;
    width: 100%;
    max-height: 400px;
}

.card-body {
    text-align: center;
}

.card-title {
    font-size: 1.5rem;
    font-family: 'Cormorant Garamond', serif;
}

.card-subtext {
    font-size: 0.9rem;
    color: #888;
}

.itinerary-cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
}

.itinerary-details {
    margin-top: 10px;
}

@media (max-width: 768px) {
    .page-title {
        font-size: 2.5rem;
    }

    .itinerary-card-large {
        width: 100%;
    }

    .itinerary-cards {
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    }
}
</style>