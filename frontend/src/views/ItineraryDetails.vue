<template>
    <div class="saved-itineraries-container">
        <h1 class="page-title">Saved Itineraries</h1>

        <div v-if="!filteredItineraries.length" class="no-itineraries-message">
            <p>No saved itineraries yet. Start creating your itinerary!</p>
        </div>

        <div v-else>
            <!-- Filter Section -->
            <div class="filter-container">
                <p class="filter-title">Filter by:</p>
                <div class="filter-options">
                    <button :class="{ 'active': selectedFilter === 'addedDate' }" @click="applyFilter('addedDate')">Added
                        Date</button>
                    <button :class="{ 'active': selectedFilter === 'country' }"
                        @click="applyFilter('country')">Country</button>
                    <button :class="{ 'active': selectedFilter === 'duration' }"
                        @click="applyFilter('duration')">Duration</button>
                </div>
            </div>

            <!-- The most recent itinerary card -->
            <div v-if="filteredItineraries.length" class="itinerary-card itinerary-card-large">
                <div class="card shadow-sm">
                    <img :src="filteredItineraries[0].image" class="card-img-top" alt="itinerary country image" />
                    <div class="card-body">
                        <h5 class="card-title">{{ filteredItineraries[0].country }}</h5>
                        <p class="card-text">
                            {{ filteredItineraries[0].numDays }}d{{ filteredItineraries[0].numDays - 1 }}n trip in {{
                                filteredItineraries[0].country }}.
                        </p>
                        <p class="card-subtext">
                            Saved on {{ new Date(filteredItineraries[0].savedAt).toLocaleDateString() }}
                        </p>
                        <button @click="toggleDetails(0)" class="btn btn-outline-primary">
                            {{ filteredItineraries[0].isExpanded ? "Hide Details" : "View Itinerary" }}
                        </button>
                    </div>
                    <div v-if="filteredItineraries[0].isExpanded" class="itinerary-details">
                        <div v-for="(day, dayIndex) in filteredItineraries[0].days" :key="dayIndex">
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
                <div v-for="(itinerary, index) in filteredItineraries.slice(1)" :key="index + 1" class="itinerary-card">
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
import { ref, computed } from "vue";
import { getFirestore, doc, getDoc } from "firebase/firestore";
import { getAuth } from "firebase/auth";
import { onMounted } from "vue";

export default {
    name: "SavedItinerary",
    setup() {
        const savedItineraries = ref([]);
        const selectedFilter = ref("addedDate");

        onMounted(async () => {
            const auth = getAuth();
            const user = auth.currentUser;
            const db = getFirestore();
            if (user) {
                const userRef = doc(db, "users", user.uid);
                const userDoc = await getDoc(userRef);
                if (userDoc.exists()) {
                    savedItineraries.value = userDoc.data().savedItineraries || [];
                }
            }
        });

        // Sorting logic
        const applyFilter = (filter) => {
            selectedFilter.value = filter;
        };

        // Computed property for filtered itineraries
        const filteredItineraries = computed(() => {
            let itineraries = [...savedItineraries.value];
            if (selectedFilter.value === "country") {
                return itineraries.sort((a, b) => a.country.localeCompare(b.country)); // Alphabetical by country
            } else if (selectedFilter.value === "duration") {
                return itineraries.sort((a, b) => b.numDays - a.numDays); // By trip duration (longest first)
            } else {
                return itineraries.sort((a, b) => new Date(b.savedAt) - new Date(a.savedAt)); // Default: by added date (most recent first)
            }
        });

        return {
            savedItineraries,
            selectedFilter,
            applyFilter,
            filteredItineraries,
        };
    },
};
</script>



<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.saved-itineraries-container {
    width: 100%;
    padding: 20px;
}

.page-title {
    text-align: center;
    font-family: 'Cormorant Garamond', sans-serif;
    font-size: 3rem;
    margin-bottom: 40px;
    font-weight: 700;
}

/* Filter Section */
.filter-container {
    margin-bottom: 30px;
    text-align: left;
    font-family: 'Inter', sans-serif;
}

.filter-title {
    margin-bottom: 10px;
    font-size: 1.2rem;
    font-weight: 500;
}

.filter-options {
    display: flex;
    gap: 10px;
}

.filter-options button {
    background-color: white;
    border: 1px solid #ddd;
    padding: 8px 15px;
    border-radius: 20px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.filter-options button.active {
    background-color: black;
    color: white;
}

.filter-options button:hover {
    background-color: #f0f0f0;
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
    margin-bottom: 10px; /* This ensures the space between the top card and others */
    padding-bottom: 10px; /* Padding for internal space */
    border: none; /* Remove the border to avoid the double border effect */
    box-shadow: none; /* Remove shadow if there is one causing extra appearance */
}

.card-body {
    text-align: center;
    font-family: 'Inter', sans-serif;
}

.card-title {
    font-size: 1.6rem;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
}

.card-text {
    font-size: 1rem;
    font-family: 'Inter', sans-serif;
    color: #666;
}

.card-subtext {
    font-size: 0.9rem;
    color: #888;
    font-family: 'Inter', sans-serif;
}

.itinerary-cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    margin-top: 20px; /* Add some margin to the top of the card grid */
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