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
                    <img :src="getCountryImage(filteredItineraries[0].country)" class="card-img-top"
                        alt="itinerary country image" />
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
                <div v-if="paginatedItineraries.length >= 1" class="hero-card"
                    @click="viewItinerary(paginatedItineraries[0].savedAt)">
                    <div class="card shadow-lg">
                        <img :src="getCountryImage(paginatedItineraries[0].country)" class="card-img-top"
                            alt="itinerary country image" />
                        <div class="gradient-overlay"></div>
                        <div class="card-body">
                            <h5 class="card-title">{{ paginatedItineraries[0].country }}</h5>
                            <p class="card-text">{{ paginatedItineraries[0].numDays }}d trip in {{
                                paginatedItineraries[0].country }}.</p>
                            <p class="card-subtext">Saved on {{ new
                                Date(paginatedItineraries[0].savedAt).toLocaleDateString() }}</p>
                        </div>
                    </div>
                </div>

                <!-- Stacked smaller cards for additional itineraries -->
                <div class="stacked-cards">
                    <div v-for="(itinerary, index) in paginatedItineraries.slice(1)" :key="index" class="small-card"
                        @click="viewItinerary(itinerary.savedAt)">
                        <img :src="getCountryImage(itinerary.country)" class="small-card-img"
                            alt="itinerary country image" />
                        <div class="small-card-text">
                            <h5>{{ itinerary.country }}</h5>
                            <p>{{ itinerary.numDays }}d trip in {{ itinerary.country }}.</p>
                            <p>Saved on {{ new Date(itinerary.savedAt).toLocaleDateString() }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Pagination buttons if more than 5 itineraries exist -->
            <div v-if="filteredItineraries.length > itemsPerPage" class="scroll-buttons">
                <button class="round-button" @click="scrollLeft" v-if="showLeftButton">&lt;</button>
                <button class="round-button" @click="scrollRight" v-if="showRightButton">&gt;</button>
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
        const currentPage = ref(0); // Track the current page for pagination
        const itemsPerPage = 5; // Number of items to show at a time
        const countries = ref([
            {
                name: "France",
                place: "Paris",
                code: "FR",
                image: require("@/assets/countries/france.jpeg"),
                description:
                    "France is known for its rich culture, art, and history, including landmarks like the Eiffel Tower.",
            },
            {
                name: "Italy",
                code: "IT",
                place: "Rome",
                image: new URL('@/assets/countries/italy.jpeg', import.meta.url).href,
                description:
                    "Rome is the cradle of Western civilization, home to iconic sites like the Colosseum and the Vatican.",

            },
            {
                name: "Japan",
                code: "JP",
                place: "Kyoto",
                image: require("@/assets/countries/japan.jpg"),
                description:
                    "Kyoto is the heart of Japan's traditional culture, renowned for its temples, gardens, and geisha districts.",
            },
            {
                name: "United States",
                code: "US",
                place: "New York",
                image: require("@/assets/countries/united_states.jpg"),
                description:
                    "The United States boasts a diverse landscape, from the skyscrapers of New York to the Grand Canyon.",
            },
            {
                name: "Spain",
                code: "ES",
                place: "Barcelona",
                image: require("@/assets/countries/spain.jpg"),
                description:
                    "Spain is famed for its passionate flamenco music, stunning beaches, and delicious tapas.",
            },
            {
                name: "China",
                code: "CN",
                place: "Beijing",
                image: require("@/assets/countries/china.jpg"),
                description:
                    "China is a land of ancient wonders, from the Great Wall to bustling cities like Beijing and Shanghai.",
            },
            {
                name: "Mexico",
                code: "MX",
                place: "Yuacatan",
                image: require("@/assets/countries/mexico.jpg"),
                description:
                    "Mexico offers vibrant culture, ancient ruins like Chichen Itza, and beautiful beaches along its coastlines.",
            },
            {
                name: "United Kingdom",
                code: "GB",
                place: "London",
                image: require("@/assets/countries/united_kingdom.jpg"),
                description:
                    "The United Kingdom is rich in history, from the Tower of London to the Highlands of Scotland.",
            },
            {
                name: "Germany",
                code: "DE",
                place: "Berlin",
                image: require("@/assets/countries/germany.jpg"),
                description:
                    "Germany is known for its medieval castles, scenic forests, and the vibrant city of Berlin.",
            },
            {
                name: "Thailand",
                code: "TH",
                place: "Bangkok",
                image: require("@/assets/countries/thailand.jpg"),
                description:
                    "Thailand is a tropical paradise, renowned for its temples, beaches, and street food culture.",
            },
            {
                name: "Turkey",
                code: "TR",
                place: "Istanbul",
                image: require("@/assets/countries/turkey.jpg"),
                description:
                    "Turkey bridges Europe and Asia, offering ancient ruins, vibrant bazaars, and stunning coastlines.",
            },
            {
                name: "Australia",
                code: "AU",
                palce: "Sydney",
                image: require("@/assets/countries/australia.jpg"),
                description:
                    "Australia is famous for its outback adventures, Great Barrier Reef, and cosmopolitan cities like Sydney.",
            },
            {
                name: "Brazil",
                code: "BR",
                place: "Rio de Janeiro",
                image: require("@/assets/countries/brazil.jpg"),
                description:
                    "Brazil is home to the Amazon rainforest, the vibrant Carnival festival, and iconic landmarks like Christ the Redeemer.",
            },
            {
                name: "Canada",
                code: "CA",
                place: "Ontario",
                image: require("@/assets/countries/canada.jpg"),
                description:
                    "Canada offers breathtaking landscapes, from the Rocky Mountains to Niagara Falls, and diverse cities.",
            },
            {
                name: "India",
                code: "IN",
                place: "Jaipur",
                image: require("@/assets/countries/india.jpg"),
                description:
                    "India is a land of contrasts, known for its ancient temples, bustling cities, and the majestic Taj Mahal.",
            },
            {
                name: "South Africa",
                code: "ZA",
                place: "Cape Town",
                image: require("@/assets/countries/south_africa.jpg"),
                description:
                    "South Africa offers diverse wildlife, beautiful landscapes, and vibrant cities like Cape Town.",
            },
            {
                name: "Russia",
                code: "RU",
                place: "Moscow",
                image: require("@/assets/countries/russia.jpg"),
                description:
                    "Russia, the largest country in the world, is known for its grand palaces, vast wilderness, and rich history.",
            },
            {
                name: "Argentina",
                code: "AR",
                place: "Buenos Aires",
                image: require("@/assets/countries/argentina.jpg"),
                description:
                    "Argentina is famous for its tango, vast pampas, and breathtaking Patagonia region.",
            },
            {
                name: "Netherlands",
                code: "NL",
                place: "Amsterdam",
                image: require("@/assets/countries/netherlands.jpg"),
                description:
                    "The Netherlands is known for its picturesque canals, tulip fields, and windmills.",
            },
            {
                name: "Greece",
                code: "GR",
                place: "Santorini",
                image: require("@/assets/countries/greece.jpg"),
                description:
                    "Greece is the birthplace of democracy, known for its ancient ruins, crystal-clear waters, and islands.",
            },
            {
                name: "Malaysia",
                code: "MY",
                place: "Kuala Lumpur",
                image: require("@/assets/countries/malaysia.jpg"),
                description:
                    "Malaysia offers a mix of modern cities, lush rainforests, and stunning beaches.",
            },
            {
                name: "Egypt",
                code: "EG",
                place: "Cairo",
                image: require("@/assets/countries/egypt.jpg"),
                description:
                    "Egypt is the land of the pharaohs, with awe-inspiring pyramids, temples, and the Nile River.",
            },
            {
                name: "Switzerland",
                code: "CH",
                place: "Zermatt",
                image: require("@/assets/countries/switzerland.jpg"),
                description:
                    "Switzerland is renowned for its alpine scenery, luxury watches, and delicious chocolates.",
            },
            {
                name: "Indonesia",
                code: "ID",
                place: "Bali",
                image: require("@/assets/countries/indonesia.jpg"),
                description:
                    "Indonesia, an archipelago of over 17,000 islands, offers diverse cultures, volcanoes, and beautiful beaches.",
            },
            {
                name: "Portugal",
                code: "PT",
                place: "Lagos",
                image: require("@/assets/countries/portugal.jpg"),
                description:
                    "Portugal is known for its stunning coastlines, historic cities like Lisbon, and world-class wine.",
            },
            {
                name: "Austria",
                code: "AT",
                place: "Vienna",
                image: require("@/assets/countries/austria.jpg"),
                description:
                    "Austria is celebrated for its alpine landscapes, classical music heritage, and charming cities like Vienna.",
            },
            {
                name: "Sweden",
                code: "SE",
                place: "Stockholm",
                image: require("@/assets/countries/sweden.jpg"),
                description:
                    "Sweden is known for its innovative design, lush forests, and the picturesque city of Stockholm.",
            },
            {
                name: "Vietnam",
                code: "VN",
                place: "Hanoi",
                image: require("@/assets/countries/vietnam.jpg"),
                description:
                    "Vietnam is a Southeast Asian gem, famous for its vibrant street markets, stunning coastlines, and history.",
            },
            {
                name: "Singapore",
                code: "SG",
                place: "Singapore",
                image: require("@/assets/countries/singapore.jpg"),
                description:
                    "Singapore is a modern city-state known for its futuristic architecture, diverse cuisine, and clean streets.",
            },
            {
                name: "New Zealand",
                code: "NZ",
                place: "Kokatahi",
                image: require("@/assets/countries/new_zealand.jpg"),
                description:
                    "New Zealand is a natural wonder, offering majestic mountains, serene lakes, and vibrant Maori culture.",
            },
            {
                name: "Poland",
                code: "PL",
                place: "Krakow",
                image: require("@/assets/countries/poland.jpg"),
                description:
                    "Poland is a country rich in history, with medieval castles, Gothic cathedrals, and the bustling city of Warsaw.",
            },
            {
                name: "Morocco",
                code: "MA",
                place: "Marrakech",
                image: require("@/assets/countries/morocco.jpg"),
                description:
                    "Morocco offers exotic souks, vast deserts, and the vibrant colors of Marrakech.",
            },
            {
                name: "Philippines",
                code: "PH",
                place: "Negros Oriental",
                image: require("@/assets/countries/philippines.jpg"),
                description:
                    "The Philippines is a tropical paradise, known for its white-sand beaches and crystal-clear waters.",
            },
            {
                name: "Chile",
                code: "CL",
                place: "Torres del Paine",
                image: require("@/assets/countries/chile.jpg"),
                description:
                    "Chile stretches along the Andes and offers diverse climates, from deserts to glaciers.",
            },
            {
                name: "South Korea",
                code: "KR",
                place: "Seoul",
                image: require("@/assets/countries/south_korea.jpg"),
                description:
                    "South Korea is a fascinating blend of ancient temples, bustling cities, and cutting-edge technology.",
            },
            {
                name: "United Arab Emirates",
                code: "AE",
                place: "Dubai",
                image: require("@/assets/countries/united_arab_emirates.jpg"),
                description:
                    "The UAE is known for its luxury, with futuristic cities like Dubai and the vast Arabian desert.",
            },
            {
                name: "Czech Republic",
                code: "CZ",
                place: "Prague",
                image: require("@/assets/countries/czech_republic.jpg"),
                description:
                    "The Czech Republic is famous for its medieval towns, Gothic architecture, and Prague's historic charm.",
            },
            {
                name: "Saudi Arabia",
                code: "SA",
                place: "Mecca",
                image: require("@/assets/countries/saudi_arabia.jpg"),
                description:
                    "Saudi Arabia is home to both the birthplace of Islam and stunning desert landscapes.",
            },
            {
                name: "Belgium",
                code: "BE",
                place: "Brussels",
                image: require("@/assets/countries/belgium.jpg"),
                description:
                    "Belgium is known for its medieval towns, Renaissance architecture, and delicious chocolates.",
            },
            {
                name: "Israel",
                code: "IL",
                place: "Jerusalem",
                image: require("@/assets/countries/israel.jpg"),
                description:
                    "Israel is a sacred land for many religions, with historical sites in Jerusalem and modern cities like Tel Aviv.",
            },
            {
                name: "Peru",
                code: "PE",
                place: "Machu Picchu",
                image: require("@/assets/countries/peru.jpg"),
                description:
                    "Peru is famous for Machu Picchu, ancient Inca history, and stunning Andean landscapes.",
            },
            {
                name: "Norway",
                code: "NO",
                place: "Tromso",
                image: require("@/assets/countries/norway.jpg"),
                description:
                    "Norway is a land of fjords, northern lights, and pristine wilderness, perfect for outdoor enthusiasts.",
            },
            {
                name: "Denmark",
                code: "DK",
                place: "Copenhagen",
                image: require("@/assets/countries/denmark.jpg"),
                description:
                    "Denmark is known for its charming cities, innovative design, and Viking history.",
            },
            {
                name: "Hungary",
                code: "HU",
                place: "Budapest",
                image: require("@/assets/countries/hungary.jpg"),
                description:
                    "Hungary is a land of thermal baths, Gothic architecture, and the beautiful capital of Budapest.",
            },
            {
                name: "Ireland",
                code: "IE",
                place: "Giant's Causeway",
                image: require("@/assets/countries/ireland.jpg"),
                description:
                    "Ireland is known for its lush green landscapes, rich folklore, and historic cities like Dublin.",
            },
            {
                name: "Finland",
                code: "FI",
                place: "Rovaniemi",
                image: require("@/assets/countries/finland.jpg"),
                description:
                    "Finland is famous for its thousands of lakes, northern lights, and cutting-edge technology.",
            },
            {
                name: "Colombia",
                code: "CO",
                place: "Bogota",
                image: require("@/assets/countries/colombia.jpg"),
                description:
                    "Colombia offers a diverse range of attractions, from coffee plantations to vibrant cities like Bogotá.",
            },
            {
                name: "Ukraine",
                code: "UA",
                place: "Kyiv",
                image: require("@/assets/countries/ukraine.jpg"),
                description:
                    "Ukraine is a country of rich history and beautiful landscapes, with Kyiv's stunning cathedrals and ancient sites.",
            },
        ]);


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

        // find country image based on the itinerary's country
        const getCountryImage = (countryName) => {
            const country = countries.value.find((c) => c.name === countryName);
            return country ? country.image : "@/assets/placeholder.jpg"; // Use placeholder if country not found
        };

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

        // Paginated itineraries based on current page
        const paginatedItineraries = computed(() => {
            const start = currentPage.value * itemsPerPage;
            const end = start + itemsPerPage;
            return filteredItineraries.value.slice(start, end);
        });

        // // Filtered and paginated itineraries
        // const filteredItineraries = computed(() => {
        //     return savedItineraries.value.slice(currentIndex.value, currentIndex.value + itemsPerPage);
        // });
        watch(savedItineraries, () => {
            currentPage.value = 0; // Reset to the first page
        });

        // Scroll functions
        const scrollLeft = () => {
            if (currentPage.value > 0) {
                currentPage.value--;
            }
        };

        const scrollRight = () => {
            if ((currentPage.value + 1) * itemsPerPage < filteredItineraries.value.length) {
                currentPage.value++;
            }
        };

        // Debugging logs
        watch([paginatedItineraries, showLeftButton, showRightButton], () => {
            console.log("Current page:", currentPage.value);
            console.log("Paginated itineraries:", paginatedItineraries.value);
            console.log("Show left button:", showLeftButton.value);
            console.log("Show right button:", showRightButton.value);
        });

        // Button visibility based on currentPage and total items
        const showLeftButton = computed(() => currentPage.value > 0);
        const showRightButton = computed(() => (currentPage.value + 1) * itemsPerPage < filteredItineraries.value.length);

        return {
            savedItineraries,
            filteredItineraries,
            paginatedItineraries,
            viewItinerary,
            selectedFilter,
            getCountryImage,
            countries,
            scrollLeft,
            scrollRight,
            showLeftButton,
            showRightButton,
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
