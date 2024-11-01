<template>

    <div class="container-fluid p-0">
        <div class="header_container">
            <div class="content">
                <h1>Travel the world</h1>
                <h4>Start Exploring | Plan your trips</h4>
            </div>
        </div>
        <!-- Section 1 -->
        <div class="d-flex flex-column flex-lg-row position-relative headerbox">
            <div class="col-lg-4 col-md-12 col-sm-12 p-0 one" @click="viewDestinations">
                <a href="#" class="section-link">
                    <img src="@/assets/countries/singapore.jpg" alt="Image 1" class="img-fluid w-100" />
                    <div class="overlay-text">Discover New Locations</div>
                    <div class="gradientoverlay"></div>
                </a>
            </div>
            <div class="col-lg-4 col-md-12 col-sm-12 p-0 one d-none d-md-block" @click="viewSavedPlaces">
                <div class="gradientoverlay"></div>
                <a href="#" class="section-link">
                    <img src="@/assets/countries/united_arab_emirates.jpg" alt="Image 2" class="img-fluid w-100" />
                    <div class="overlay-text">Browse Your Saved Locations</div>
                </a>
            </div>
            <div class="col-lg-4 col-md-12 col-sm-12 p-0 one d-none d-md-block" @click="viewMainPage">
                <div class="gradientoverlay"></div>
                <a href="#" class="section-link">
                    <img src="@/assets/countries/austria.jpg" alt="Image 3" class="img-fluid w-100" />
                    <div class="overlay-text">Enter a TikTok Link!</div>
                </a>
            </div>
        </div>
    </div>







    <!-- <div class="sticky-top">
        <div class="row justify-content-between align-items-center sticky-header g-0">
            <div class="col-3 date-column">
                <h2 class="page-title">My Itineraries</h2>
                <div class="filter-dropdown d-flex align-items-center">
                    <select v-model="selectedFilter" @change="filterPlaces" class="form-select me-2">
                        <option value="">Select Filter</option>
                        <option value="alphabetical">Filter by Alphabet</option>
                        <option value="recently-added">Filter by Recently Added</option>
                    </select>
                    <button @click="deleteAllPlaces" :disabled="isDeleteAllDisabled" class="btn btn-delete-all">
                        Delete All
                    </button>
                </div>
            </div>
            <div class="col-auto generateButton">
                <button @click="toggleModal" type="button" class="btn view-itinerary-btn">View
                    Itinerary</button>
                <button @click="navigateToGeneratedItinerary" type="button" class="btn view-full-itinerary-btn">View
                    Full
                    Itinerary</button>
            </div>
        </div>
    </div> -->

    <div class="saved-itineraries-container">
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

            <div v-else class="itineraries-grid multiple responsive-container">
                <!-- Hero card for the first itinerary -->
                <div class="hero-card" @click="viewItinerary(filteredItineraries[0].savedAt)">
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

                <div class="stacked-cards-wrapper">
                    <!-- Scrollable container for additional itineraries -->
                    <div class="stacked-cards">
                        <div v-for="(itinerary, index) in paginatedSmallItineraries" :key="index" class="small-card"
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

                    <!-- Pagination buttons if more than 5 itineraries exist -->
                    <div v-if="true" class="scroll-buttons">
                        <button class="round-button" @click="scrollLeft">&lt;</button>
                        <button class="round-button" @click="scrollRight">&gt;</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import { ref, computed, watch } from "vue";
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
            console.log("Initial filteredItineraries:", filteredItineraries.value);
            const auth = getAuth();
            const user = auth.currentUser;
            const db = getFirestore();
            if (user) {
                const userRef = doc(db, "users", user.uid);
                const userDoc = await getDoc(userRef);
                if (userDoc.exists()) {
                    savedItineraries.value = userDoc.data().savedItineraries || [];
                    console.log("Loaded Itineraries:", savedItineraries.value); // Check if data is loaded correctly
                } else {
                    console.log("User document does not exist");
                }
            } else {
                console.log("User is not logged in");
            }
        });

        watch(savedItineraries, (newVal) => {
            console.log("savedItineraries updated:", newVal);
        });

        //map country to continent
        const getContinent = (country) => {
            const continentMapping = {
                France: "Europe",
                Italy: "Europe",
                Japan: "Asia",
                "United States": "North America",
                Spain: "Europe",
                China: "Asia",
                Mexico: "North America",
                "United Kingdom": "Europe",
                Germany: "Europe",
                Thailand: "Asia",
                Turkey: "Asia/Europe",
                Australia: "Oceania",
                Brazil: "South America",
                Canada: "North America",
                India: "Asia",
                "South Africa": "Africa",
                Russia: "Europe/Asia",
                Argentina: "South America",
                Netherlands: "Europe",
                Greece: "Europe",
                Malaysia: "Asia",
                Egypt: "Africa",
                Switzerland: "Europe",
                Indonesia: "Asia",
                Portugal: "Europe",
                Austria: "Europe",
                Sweden: "Europe",
                Vietnam: "Asia",
                Singapore: "Asia",
                "New Zealand": "Oceania",
                Poland: "Europe",
                Morocco: "Africa",
                Philippines: "Asia",
                Chile: "South America",
                "South Korea": "Asia",
                "United Arab Emirates": "Asia",
                "Czech Republic": "Europe",
                "Saudi Arabia": "Asia",
                Belgium: "Europe",
                Israel: "Asia",
                Peru: "South America",
                Norway: "Europe",
                Denmark: "Europe",
                Hungary: "Europe",
                Ireland: "Europe",
                Finland: "Europe",
                Colombia: "South America",
                Ukraine: "Europe",
            };
            // Standardize the country name format
            const formattedCountry = country?.trim().replace(/\s+/g, " ");
            const continent = continentMapping[formattedCountry] || "Unknown";
            console.log(`Mapping for country: ${formattedCountry}, Continent: ${continent}`);
            return continent
        };

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

        //redirecting to the itinerary when clicked
        const viewDestinations = () => {
            router.push({
                name: 'MyDestinations',
            });
        };

        //redirecting to the itinerary when clicked
        const viewSavedPlaces = () => {
            router.push({
                name: 'SavedPlaces',
            });
        };

        //redirecting to the itinerary when clicked
        const viewMainPage = () => {
            router.push({
                name: 'MainPage',
            });
        };

        const filteredItineraries = computed(() => {
            if (!savedItineraries.value || savedItineraries.value.length === 0) {
                console.log("No saved itineraries to filter.");
                return [];
            }

            let itineraries = [...savedItineraries.value];
            const sortedItineraries = itineraries.sort((a, b) => new Date(b.savedAt) - new Date(a.savedAt));
            console.log("Sorted itineraries:", sortedItineraries);
            return sortedItineraries;
        });


        // Watch to see if filteredItineraries updates as expected
        watch(filteredItineraries, (newVal, oldVal) => {
            console.log("filteredItineraries updated:");
            console.log("New value:", newVal);
            console.log("Old value:", oldVal);
        });

        watch(savedItineraries, (newVal, oldVal) => {
            console.log("savedItineraries updated:", newVal);
            console.log("Previous savedItineraries:", oldVal);
        });

        watch(selectedFilter, (newFilter) => {
            console.log("Selected filter changed:", newFilter);
        });

        const filterPlaces = (event) => {
            selectedFilter.value = event.target.value;
            console.log("Filter applied:", selectedFilter.value);
        };

        // Paginated itineraries based on current page
        const paginatedSmallItineraries = computed(() => {
            const start = currentPage.value * (itemsPerPage - 1) + 1;
            const end = start + (itemsPerPage - 1);
            const pageData = filteredItineraries.value.slice(start, end);
            console.log("Paginated Itineraries for Page:", currentPage.value, pageData); // Check paginated data
            return pageData;
        });


        // Scroll functions
        const scrollLeft = () => {
            if (currentPage.value > 0) {
                currentPage.value--;
                console.log("Scrolled left:", currentPage.value);
            } else {
                console.log("Cannot scroll left, already at first page");
            }
        };

        const scrollRight = () => {
            if ((currentPage.value + 1) * itemsPerPage < filteredItineraries.value.length) {
                currentPage.value++;
                console.log("Scrolled right:", currentPage.value);
            } else {
                console.log("Cannot scroll right, reached last page");
            }
        };


        // Debugging logs
        // watch([paginatedItineraries, showLeftButton, showRightButton], () => {
        //     console.log("Current page:", currentPage.value);
        //     console.log("Paginated itineraries:", paginatedItineraries.value);
        //     console.log("Show left button:", showLeftButton.value);
        //     console.log("Show right button:", showRightButton.value);
        // });

        // Button visibility based on currentPage and total items
        const showLeftButton = computed(() => {
            const canScrollLeft = currentPage.value > 0;
            console.log("Show Left Button:", canScrollLeft, "Current Page:", currentPage.value);
            return canScrollLeft;
        });

        const showRightButton = computed(() => {
            const remainingItems = filteredItineraries.value.length - 1 - (currentPage.value + 1) * (itemsPerPage - 1);
            return remainingItems > 0;
        });



        return {
            getContinent,
            savedItineraries,
            filteredItineraries,
            paginatedSmallItineraries,
            viewItinerary,
            viewDestinations,
            viewSavedPlaces,
            viewMainPage,
            selectedFilter,
            filterPlaces,
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
/* ******************** header  container ******************* */
/* General styling for grid items */
.container-fluid {
    position: relative;
    max-width: 100vw;
    overflow: hidden;
    margin-bottom: 90px;
}

.header_container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    z-index: 1;
    text-align: center;
    color: white;
    z-index: 3;
}

.content h1 {
    font-size: 6rem;
    font-weight: 700;
}

.content h4 {
    color: white;
    font-size: 1.5rem;
    font-weight: 500;

}

.headerbox {
    height: 60vh;
    /* Fixed height to ensure images have a base to fill */
    display: flex;
}

.col-lg-4,
.col-md-12,
.col-sm-12 {
    height: 100%;
    /* Make columns fill headerbox height */
}

.section-link {
    position: relative;
    display: inline-block;
    color: white;
    text-decoration: none;
    height: 100%;
    width: 100%;
    /* Full width */
}

.img-fluid {
    width: 100%;
    height: 100%;
    object-fit: cover;
    /* Ensures the image fills the container without distortion */
    object-position: center;
    /* Center image within container */
}

.overlay-text {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    padding: 10px;
    color: white;
    font-weight: bold;
    text-align: center;
    z-index: 2;
}

.gradientoverlay {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.2);
    /* Replace gradient with a solid black with opacity */
    transition: background-color 0.3s ease;
    /* Smooth transition for brightness on hover */
    z-index: 1;
}

.one:hover .gradientoverlay {
    background-color: rgba(0, 0, 0, 0.0);
    /* Make overlay lighter on hover */
}

.one {
    transition: transform 0.3s ease, background-color 0.3s ease;
    /* Smooth transition */
}

.one:hover {
    transform: scale(1.05);
    /* Slightly scale up the card */
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    /* Add a stronger shadow */
}


/* ******************** stickbar container ******************* */
/* header sicky styling */
.sticky-top {
    position: sticky;
    top: 0;
    background-color: white;
    z-index: 1100;
    padding: 10px 5%;
    border-bottom: 1px solid lightgrey;
    margin-bottom: 80px;
}

.date-column {
    text-align: left;
    padding-left: 15px;
    /* Increase padding to move it left */
    font-family: 'Roboto', sans-serif;
    /* Change to your desired font */
    font-size: 1.5rem;
    /* Adjust font size if necessary */
    margin-top: 10px;
    margin-bottom: 10px;
}

.generateButton {
    text-align: right;
    padding-right: 5%;
    font-size: 1.5rem;
    margin-top: 10px;
    margin-bottom: 10px;
}

.empty-message {
    text-align: center;
    font-size: 1.2rem;
    color: grey;
    margin-top: 20px;
}

.close-button {
    position: absolute;
    top: 10px;
    /* Adjust as needed */
    right: 10px;
    /* Adjust as needed */
    background: transparent;
    /* No background */
    border: none;
    /* No border */
    color: white;
    /* Color of the 'X' */
    font-size: 1.2rem;
    /* Adjust size */
    cursor: pointer;
    /* Pointer cursor */
    z-index: 1;
    /* Ensure it is on top */
}

.close-button:hover {
    background: transparent;
    color: red;

    /* Change color on hover */
}

.filter-dropdown {
    margin: 10px 0;

}

.filter-dropdown .form-select {
    width: 100%;
    border-radius: 100px;
    border: 1px solid black;
}

.btn-delete-all {
    width: 200px;
    border-radius: 30px;
    border: 1px solid black;
    color: black;
    background-color: #ffffff;
    transition: background-color 0.3s ease;
    /* Apply smooth transition */
}

.btn {
    /* Set button color to black */
    color: white;
    /* Keep the text color white for contrast */
    border: none;
    /* Remove default border */
}

.btn:hover {
    background-color: #0057d9;
    /* Darker color on hover for visual feedback */
    color: white;
    /* Keep the text color white on hover */
}

.close-modal-btn:hover {
    color: white;
    /* Keep the text color white on hover */
}

.close-modal-btn {
    background-color: #0057d9;
}

.view-itinerary-btn {
    margin-right: 10px;
    background-color: #ffffff;
    border-radius: 100px;
    margin-top: 30px;
    border: 1px solid black;
    color: black;
    /* Adjust space as needed */
    transition: background-color 0.3s ease;
    /* Apply smooth transition */

}

.view-full-itinerary-btn {
    background-color: #ffffff;
    border-radius: 100px;
    margin-top: 30px;
    border: 1px solid black;
    color: black;
    transition: background-color 0.3s ease;
    /* Apply smooth transition */

}


/* ***************** saved itinerary container *************** */
/* ************************************************ */
/* Page layout styling */
.saved-itineraries-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    margin: 0 auto;
    width: 100%;
    max-width: 1400px;
    /* Increased max width */
}

.page-title {
    text-align: left;
    font-size: 2rem;
    font-family: 'Cormorant Garamond', serif;
    font-weight: bolder;
    margin-bottom: 15px;
    width: 100%;
    padding-left: 2px;
    box-sizing: border-box;
}


.single {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    max-width: 1200px;
    /* Controls the width of the entire card layout */
    margin: 0 auto;
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
    flex-direction: column;
    width: 100%;
    max-width: 1200px;
    /* Controls the width of the entire card layout */
    margin: 0 auto;
}

.itineraries-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    /* Adjusted column width ratio */
    gap: 20px;
    width: 100%;
    /* Set to full width of container */
    max-width: 1400px;
    /* Increased max width to match container */
    justify-content: center;
}

/* ************************************************ */
/* single card styling */

.single-itinerary-card {
    width: 100%;
    /* Adjust width to take a larger space */
    max-width: 900px;
    /* Limit the maximum width */
    margin: 20px 0;
    /* Add spacing above and below */
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    /* Optional styling for shadow */
    border-radius: 8px;
    /* Optional rounded corners */
}

.card {
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden;
}

.card-img-top {
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
    background: linear-gradient(to top, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0) 70%);
    z-index: 1;
}

.single-itinerary-card {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}


.single-itinerary-card .card-body {
    position: absolute;
    bottom: 20px;
    left: 20px;
    z-index: 2;
    color: white;
    padding: 10px;
    box-sizing: border-box;

}

.single-itinerary-card .card-title {
    font-size: 3rem;
    padding-left: 6px;
    margin: 0;
}

.single-itinerary-card .card-text {
    font-size: 1rem;
    color: white;
    margin-top: 5px;
}

.single-itinerary-card .card-subtext {
    font-size: 1rem;
    color: white;
    margin-top: 5px;
    padding-left: 3px;
}

.single-itinerary-card:hover {
    transform: scale(1.05);
    /* Slightly scale up the card */
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    /* Add a stronger shadow */
}




/* ************************************************ */




/*more than one itinerary styling*/
/* Hero card styling */
.hero-card {
    height: 550px;
    width: 100%;
    display: flex;
    align-items: center;
    position: relative;
    overflow: hidden;
    border-radius: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    /* Smooth transition */
}

.hero-card:hover {
    transform: scale(1.05);
    /* Slightly scale up the card */
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    /* Add a stronger shadow */
}

.hero-card .card {
    position: relative;
    width: 100%;
    height: 100%;
    border-radius: 30px;
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
}

.hero-card .card-body {
    position: absolute;
    bottom: 0;
    color: white;
    padding: 20px;
    width: 100%;
    box-sizing: border-box;
    z-index: 2;
}


.hero-card .card-body .card-title {
    font-size: 3rem;
    margin-bottom: 10px;
}

.hero-card .card-text {
    font-size: 1.2rem;
    color: white;
    margin-top: 5px;
}

.hero-card .card-subtext {
    font-size: 1rem;
    color: white;
    margin-top: 2px;
    opacity: 0.8;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
}

/* Wrapper to position buttons at bottom right */
.stacked-cards-wrapper {
    position: relative;
    /* Allow absolute positioning within */
    /* padding-bottom: 60px; */
}

/* Stacked small cards styling */
.stacked-cards {
    display: flex;
    flex-direction: column;
    gap: 15px;
    /* justify-content: flex-start; Ensures small cards stack at the top */
    align-self: flex-start;
    -webkit-scroll-snap-type: x mandatory;
    -ms-scroll-snap-type: x mandatory;
    scroll-snap-type: x mandatory;
    scroll-behavior: smooth;
    -webkit-overflow-scrolling: touch;
    -ms-overflow-style: none;
    scrollbar-width: none;
    scroll-padding-right: 32px;
}

.small-card {
    display: flex;
    align-items: center;
    width: 100%;
    padding: 10px;
    background: rgb(234, 250, 255);
    border-radius: 30px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    /* Smooth transition */
}

.small-card:hover {
    transform: scale(1.05);
    /* Slightly scale up the card */
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    /* Add a stronger shadow */
}

.small-card-img {
    width: 100px;
    height: 106px;
    object-fit: cover;
    border-radius: 20px;
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
    position: absolute;
    bottom: -80px;
    right: 5px;
    display: flex;
    gap: 10px;
    padding-bottom: 20px;
}


.round-button {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    padding-bottom: 7px;
    border: 2px solid #b9b9b9;
    background-color: transparent;
    color: #888;
    font-size: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
}

.round-button:hover {
    border-color: #666;
    color: #666;
}

.round-button:focus {
    outline: none;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
}


/* ******************************************* */
/* viewport sizes */
@media (max-width: 1200px) {
    .overlay-text {
        font-size: 1.2rem;
    }

    .content h1 {
        font-size: 6rem;
    }

    .content h4 {
        font-size: 1.5rem;
    }
}

@media (max-width: 992px) {
    .overlay-text {
        font-size: 1rem;
    }

    .content h1 {
        font-size: 3rem;
    }

    .content h4 {
        font-size: 1.2rem;
    }
}

@media (max-width: 768px) {
    .overlay-text {
        font-size: 1rem;
    }

    .content h1 {
        font-size: 2rem;
    }

    .content h4 {
        font-size: 1rem;
    }

    .itineraries-grid {
        display: flex;
        flex-direction: column;
        align-items: stretch;
    }

    .stacked-cards-wrapper {
        width: 100%;
        margin-top: 20px;
    }

    .small-card {
        width: 100%;
        max-width: 100%;
        margin: 0 auto;
        box-sizing: border-box;
    }

    .scroll-buttons {
        position: static;
        margin-top: 10px;
        display: flex;
        justify-content: center;
    }
}
</style>
