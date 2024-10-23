<template>
    <div class="itinerary-page">
        <div class="sticky-header">
            <div class="back-button-container">
                <button @click="goBack" class="back-button">← Back</button>
            </div>
            <h2 class="header-title">Your Itinerary</h2>
            <div class="header-buttons">
                <button @click="removeAllPlaces" class="remove-all-button">Remove All</button>
                <button @click="generateItinerary" class="generate-button">Generate Itinerary</button>
            </div>
        </div>
        <div v-if="itineraryPlaces.length === 0">
            <p>No places in the itinerary.</p>
        </div>
        <div class="itinerary-grid">
            <div v-for="place in itineraryPlaces" :key="place.place_id" class="place-card">
                <img :src="place.image" alt="Image of {{ place.name }}" class="place-image" />
                <div class="place-info">
                    <h3 class="place-name">{{ place.name }}</h3>
                    <p class="place-location">{{ place.vicinity }}, {{ place.country }}</p>
                    <button @click="removePlace(place.place_id)" class="remove-button">✖</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getFirestore, doc, getDoc, updateDoc } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';

export default {
    name: 'MyItinerary',
    setup() {
        const itineraryPlaces = ref([]);
        const db = getFirestore();
        const auth = getAuth();
        const router = useRouter();

        onMounted(async () => {
            const user = auth.currentUser;

            if (user) {
                const userDocRef = doc(db, 'users', user.uid);
                const userDoc = await getDoc(userDocRef);

                if (userDoc.exists()) {
                    const data = userDoc.data();
                    itineraryPlaces.value = data.generatedItineraries || [];
                }
            }
        });

        const removePlace = async (placeId) => {
            itineraryPlaces.value = itineraryPlaces.value.filter(place => place.place_id !== placeId);
            await updateItineraryInFirestore();
        };

        const removeAllPlaces = async () => {
            itineraryPlaces.value = [];
            await updateItineraryInFirestore();
        };

        const generateItinerary = () => {
            router.push({
                name: 'GeneratedItinerary',
            });
        };

        const goBack = () => {
            router.go(-1);
        };

        const updateItineraryInFirestore = async () => {
            const user = auth.currentUser;
            if (user) {
                const userDocRef = doc(db, 'users', user.uid);
                await updateDoc(userDocRef, { generatedItineraries: itineraryPlaces.value });
            }
        };

        return { itineraryPlaces, removePlace, removeAllPlaces, generateItinerary, goBack };
    }
};
</script>

<style scoped>
h2 {
    font-family: 'Cormorant Garamond', serif;
    font-weight: bolder;
}

.itinerary-page {
    padding: 20px;
}

.sticky-header {
    position: sticky;
    top: 0;
    background-color: #fff;
    padding: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
}

.back-button-container {
    flex: 1;
}

.header-title {
    flex: 1;
    text-align: center;
    margin: 0;
}

.header-buttons {
    display: flex;
    gap: 10px;
    flex: 1;
    justify-content: flex-end;
}

.itinerary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

.place-card {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    position: relative;
    transition: transform 0.3s;
}

.place-card:hover {
    transform: translateY(-5px);
}

.place-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
}

.place-info {
    padding: 15px;
}

.place-name {
    font-size: 1.2rem;
    margin: 0 0 5px;
}

.place-location {
    color: #666;
    margin: 0;
}

.remove-button {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 20px;
    color: #ff0000;
    cursor: pointer;
}

.remove-all-button,
.generate-button {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.remove-all-button {
    background-color: black;
    color: white;
}

.generate-button {
    background-color: black;
    color: white;
}
</style>
