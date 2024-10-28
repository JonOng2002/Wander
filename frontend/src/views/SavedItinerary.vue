<template>
    <div class="saved-itineraries-container">
        <h1 class="page-title">My Itineraries</h1>

        <div v-if="!filteredItineraries.length" class="no-itineraries-message">
            <p>No saved itineraries yet. Start creating your itinerary!</p>
        </div>

        <div v-else class="single">
            <!-- Single centered large card for one itinerary -->
            <div v-if="filteredItineraries.length === 1" class="single-itinerary-card"
                @click="viewItinerary(filteredItineraries[0].savedAt)">
                <div class="card shadow-lg">
                    <img src="../assets/placeholder.jpg" class="card-img-top" alt="itinerary country image" />
                    <div class="gradient-overlay"></div>
                    <div class="card-body">
                        <h5 class="card-title">{{ filteredItineraries[0].country }}</h5>
                        <p class="card-text">{{ filteredItineraries[0].numDays }}d trip in {{
                            filteredItineraries[0].country }}</p>
                        <p class="card-subtext">Saved on {{ new
                            Date(filteredItineraries[0].savedAt).toLocaleDateString() }}</p>
                    </div>
                </div>
            </div>

            <div v-else class="itineraries-grid multiple">
                <!-- Hero card for the first itinerary -->
                <div v-if="filteredItineraries.length >= 1" class="hero-card"
                    @click="viewItinerary(filteredItineraries[0].savedAt)">
                    <div class="card shadow-lg">
                        <img src="../assets/placeholder.jpg" class="card-img-top" alt="itinerary country image" />
                        <div class="gradient-overlay"></div>
                        <div class="card-body">
                            <h5 class="card-title">{{ filteredItineraries[0].country }}</h5>
                            <p class="card-text">{{ filteredItineraries[0].numDays }}d trip in {{
                                filteredItineraries[0].country }}.</p>
                            <p class="card-subtext">Saved on {{ new
                                Date(filteredItineraries[0].savedAt).toLocaleDateString() }}</p>
                        </div>
                    </div>
                </div>

                <!-- Stacked smaller cards for additional itineraries -->
                <div class="stacked-cards">
                    <div v-for="(itinerary, index) in filteredItineraries.slice(1, 5)" :key="index" class="small-card"
                        @click="viewItinerary(itinerary.savedAt)">
                        <img src="../assets/placeholder.jpg" class="small-card-img" alt="itinerary country image" />
                        <div class="small-card-text">
                            <h5>{{ itinerary.country }}</h5>
                            <p>{{ itinerary.numDays }}d trip in {{ itinerary.country }}.</p>
                            <p>Saved on {{ new Date(itinerary.savedAt).toLocaleDateString() }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Pagination buttons if more than 4 itineraries exist -->
            <div v-if="filteredItineraries.length > 5" class="scroll-buttons">
                <button class="round-button" @click="scrollLeft">&lt;</button>
                <button class="round-button" @click="scrollRight">&gt;</button>
            </div>
        </div>
    </div>
</template>


<script>
import { ref, computed } from "vue";
import { getFirestore, doc, getDoc } from "firebase/firestore";
import { getAuth } from "firebase/auth";
import { onMounted } from "vue";
import router from "@/router";

export default {
    name: "SavedItinerary",
    setup() {
        const savedItineraries = ref([]);
        const selectedFilter = ref("addedDate");
        // const currentIndex = ref(0); // Track the starting index for the visible itineraries
        // const itemsPerPage = 5; // Number of items to show at a time


        //loading saved itineraries from firestore
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

        //redirecting to the itinerary when clicked
        const viewItinerary = (savedAt) => {
            router.push({
                name: 'ItineraryDetails',
                params: { savedAt },
            });
        };

        const filteredItineraries = computed(() => {
            let itineraries = [...savedItineraries.value];
            return itineraries.sort((a, b) => new Date(b.savedAt) - new Date(a.savedAt));
        });

        // // Filtered and paginated itineraries
        // const filteredItineraries = computed(() => {
        //     return savedItineraries.value.slice(currentIndex.value, currentIndex.value + itemsPerPage);
        // });

        //scolling left
        // const scrollLeft = () => {
        //     // Decrement index, ensuring it doesn’t go below 0
        //     if (currentIndex.value > 0) {
        //         currentIndex.value -= itemsPerPage;
        //     }
        // };

        // //scrolling right
        // const scrollRight = () => {
        //     // Increment index, ensuring it doesn’t go past the last item
        //     if (currentIndex.value + itemsPerPage < savedItineraries.value.length) {
        //         currentIndex.value += itemsPerPage;
        //     }
        // };  

        return {
            savedItineraries,
            filteredItineraries,
            viewItinerary,
            selectedFilter,
            // scrollLeft,
            // scrollRight,
            // Computed to check button visibility
            // showLeftButton: computed(() => currentIndex.value > 0),
            // showRightButton: computed(() => currentIndex.value + itemsPerPage < savedItineraries.value.length),

        };
    },
};
</script>

<style scoped>
.saved-itineraries-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    /* max-width: 1600px; */
}

/* .multiple {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
} */

.page-title {
    text-align: left;
    font-size: 3rem;
    font-family: 'Cormorant Garamond', serif;
    font-weight: bolder;
    margin-bottom: 25px;
    width: 100%;
    /* Ensures it spans the full width */
    padding-left: 20px;
    /* Adds some space from the left edge */
    box-sizing: border-box;
}

/* CSS to ensure consistent image sizing within cards */
.card-img-top {
    width: 100%;
    /* Ensures the image stretches across the card width */
    height: 100%;
    /* Ensures the image stretches across the card height */
    object-fit: cover;
    /* Crops the image to fill the container while preserving its aspect ratio */
    aspect-ratio: 5 / 3;
    /* Ensures all images have the same aspect ratio */
}

/* Centered large card when there's only one itinerary */
/* Single large card centered and filling the container */
.single-itinerary-card {
    width: 100vW;
    max-width: 800px;
    margin: 20px auto;
    height: 65vh;
    /* Adjust this value as needed for desired screen coverage */
    display: flex;
    align-items: center;
}

.single-itinerary-card .card {
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden;
    border-radius: 8px;
}

.single-itinerary-card .card-img-top {
    width: 100%;
    height: 100%;
    object-fit: cover;
}


.single-itinerary-card .gradient-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0) 80%);
    z-index: 1;
    /* Ensures the overlay sits above the image */
}

.single-itinerary-card .card-body {
    position: absolute;
    bottom: 0;
    width: 100%;
    /* background: rgba(0, 0, 0, 0.5); Dark overlay for readability */
    color: white;
    padding: 20px;
    box-sizing: border-box;
    z-index: 1;
    /* Ensures the overlay sits above the image */

}

.single-itinerary-card .card-body .card-title {
    font-size: 3rem;
    margin-bottom: 10px;
}

.itineraries-grid {
    display: grid;
    grid-template-columns: 65% 35%;
    /* Large card on left, stacked small cards on right */
    gap: 20px;
    width: 100%;
    max-width: 1600px;
    justify-content: center;

}

/* Hero card styling */
.hero-card {
    height: 550px;
    display: flex;
    align-items: center;
    position: relative;
    overflow: hidden;
    border-radius: 8px;
}

.hero-card .card {
    position: relative;
    height: 100%;
    border-radius: 8px;
    overflow: hidden;
}

.hero-card img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.hero-card .gradient-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0) 80%);
    z-index: 1;
    /* Ensures the overlay sits above the image */
}

.hero-card .card-body {
    position: absolute;
    bottom: 0;
    /* background: rgba(0, 0, 0, 0.5); Dark overlay for readability */
    color: white;
    padding: 20px;
    width: 100%;
    box-sizing: border-box;
    z-index: 1;
    /* Ensures the overlay sits above the image */
}

.hero-card .card-body .card-title {
    font-size: 3rem;
    margin-bottom: 10px;
}

/* Stacked small cards styling */
.stacked-cards {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.small-card {
    display: flex;
    align-items: center;
    padding: 10px;
    background: rgb(234, 250, 255);
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.small-card-img {
    width: 100px;
    height: 106px;
    object-fit: cover;
    border-radius: 5px;
    margin-right: 15px;
}

.small-card-text h5 {
    font-size: 1rem;
    margin: 0;
}

.small-card-text p {
    font-size: 0.875rem;
    color: #555;
    margin: 2px 0;
}

.scroll-buttons {
    display: flex;
    justify-content: right;
    margin-top: 20px;
}

.round-button {
    width: 40px;
    /* Adjust size as needed */
    height: 40px;
    border-radius: 50%;
    border: 2px solid #b9b9b9;
    /* Light gray border */
    background-color: transparent;
    color: #888;
    /* Matching gray color */
    font-size: 1.5rem;
    /* Size for the arrow */
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
    padding: 10px 10px 15px 10px;
    margin: 4px;
}

.round-button:hover {
    border-color: #666;
    /* Slightly darker gray on hover */
    color: #666;
}

.round-button:focus {
    outline: none;
    /* Removes default focus outline */
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
    /* Optional shadow for focus */
}

</style>
