<!-- src/views/DestinationDetails.vue -->
<template>

  <div class="secondary_header">
    <div class="secondary_content">
      <h2>Top Tourist Attractions in {{ country }}</h2>
      <h5>Exlpore the wonders of {{ country }}</h5>
    </div>

    <div class="dropdown-container" v-motion-slide-visible-once-top>
      <div class="dropdown">
        <button @click="goBack" class="dropdown-btn">Back to Destinations</button>
      </div>

      <div class="dropdown">
        <select v-model="sortOption" @change="updateSortCriteria" class="dropdown-btn form-select me-2"
          aria-label="Sort Attractions">
          <option value="popularity-desc">Sort By Popularity: High to Low (Default)</option>
          <option value="popularity-asc">Sort By Popularity: Low to High</option>
          <option value="rating-desc">Sort By Rating: High to Low</option>
          <option value="rating-asc">Sort By Rating: Low to High</option>

        </select>
      </div>
    </div>
  </div>

    <!-- Display Loading Indicator -->
    <div v-if="loading" class="loading">Loading...</div>

    <!-- Display Error Message -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <!-- Display Attractions List -->
    <div v-if="!loading && !errorMessage" class="card-grid">
      <transition-group name="list" tag="div" class="transition-wrapper">
        <div v-for="attraction in sortedAttractions" :key="attraction.place_id" class="card-container" v-motion-slide-visible-once-top>
          <div class="card destination-card" :style="{ backgroundImage: `url(${attraction.image || defaultImage})` }">
            <div class="overlay"></div>

            <div class="card-body">
              <h5 class="card-title">{{ attraction.name }}</h5>
              <p class="card-text">{{ attraction.vicinity }}, {{ attraction.city }}</p>

              <!-- Star Rating and Exact Number -->
              <div class="rating-section">
                <star-rating :rating="attraction.rating"></star-rating>
                <span class="rating-number">{{ attraction.rating.toFixed(1) }} / 5 </span> &nbsp;
                <span class="rating-text">( {{ attraction.user_ratings_total }} reviews)</span>
              </div>



              <!-- Save Place Button -->
              <save-place-button class="btn itinerary-button" :class="{ 'saved': isPlaceSaved(attraction.place_id) }"
                :placeId="attraction.place_id" :isAlreadySaved="isPlaceSaved(attraction.place_id)"
                @save-place="savePlaceToFirebase">
                {{ isPlaceSaved(attraction.place_id) ? 'Saved' : 'Add to Saved Places' }}
              </save-place-button>
            </div>
          </div>
        </div>
      </transition-group>
    </div>

    <!-- Added ToastNotification -->
    <ToastNotification :show="toastShow" :message="toastMessage" :type="toastType" :duration="3000"
      @update:show="toastShow = $event" />
</template>

<script>
// Import necessary components and functions
import SavePlaceButton from "@/components/SavePlaceButton.vue"; // Adjust the path as needed
import StarRating from "@/components/StarRating.vue"; // Import the StarRating component
import ToastNotification from "@/components/ToastNotification.vue";
import { auth, db } from "@/main.js"; // Adjust the path based on your project structure
import { doc, getDoc, setDoc } from "firebase/firestore";
import axios from "axios";
import defaultImage from '@/assets/placeholder.jpg'; // Correctly import the fallback image

export default {
  name: "DestinationDetails",
  components: {
    SavePlaceButton,
    StarRating,
    ToastNotification,
  },
  inject: ["savedPlacesState"], // Inject the provided global state
  data() {
    return {
      attractions: [],
      loading: true,
      country: this.$route.params.country,
      // Your Google Places API Key
      apiKey: process.env.VUE_APP_GOOGLE_API_KEY || "YOUR_GOOGLE_PLACES_API_KEY", // Replace with your actual API key or use environment variable
      cityName: this.$route.params.city || "Unknown City",
      userId: null,
      errorMessage: "", // For user-friendly error messages
      sortCriteria: {
        field: 'popularity', // 'popularity' or 'rating'
        direction: 'desc',    // 'asc' or 'desc'
      },
      toastShow: false,
      toastMessage: "",
      toastType: "info", // Default type
      defaultImage: defaultImage, // Fallback image
      countryRadius: {
        'Malaysia': 30000,     // 30 km radius for Malaysia
        'Indonesia': 30000,    // 30 km radius for Indonesia
        'Singapore': 25000,    // 30 km radius for Singapore
        // Add more countries here if needed
      },
      defaultRadius: 50000,     // Default radius of 50 km for other countries
      cityRadius: {
        'Johor Bahru': 10000,   // 10 km radius for Johor Bahru
        // Add more cities here if needed
      },
    };
  },
  created() {
    console.log(`Using API Key: ${this.apiKey}`); // Verify API key
    this.fetchAttractions();
  },
  computed: {
    countryDetails() {
      // Find the country in the list of countries
      return this.countries.find(c => c.name === this.country);
    },

    sortedAttractions() {
      return this.attractions.slice().sort((a, b) => {
        const { field, direction } = this.sortCriteria;

        if (field === 'popularity') {
          // Sort by user_ratings_total
          if (b.user_ratings_total !== a.user_ratings_total) {
            return direction === 'asc'
              ? a.user_ratings_total - b.user_ratings_total
              : b.user_ratings_total - a.user_ratings_total;
          }
        } else if (field === 'rating') {
          // Sort by rating
          if (b.rating !== a.rating) {
            return direction === 'asc'
              ? a.rating - b.rating
              : b.rating - a.rating;
          }
        }

        // If both fields are equal, maintain original order or apply a tertiary sort
        return 0;
      });
    },

    savedPlaceIds() {
      return this.savedPlacesState && Array.isArray(this.savedPlacesState.savedPlaces)
        ? new Set(this.savedPlacesState.savedPlaces.map(place => place.place_id))
        : new Set();
    },

    sortOption: {
      get() {
        return `${this.sortCriteria.field}-${this.sortCriteria.direction}`;
      },
      set(value) {
        const [field, direction] = value.split('-');
        this.sortCriteria.field = field;
        this.sortCriteria.direction = direction;
      },
    },

  },
  methods: {

    /**
 * Fetches an image from Unsplash based on a query.
 * @param {String} query - The search term for the image.
 * @returns {String} - The URL of the fetched image or a default image.
 */

    async getUnsplashImage(query) {

      const unsplashAccessKey = process.env.VUE_APP_UNSPLASH_ACCESS_KEY;

      if (!unsplashAccessKey) {
        console.error("Unsplash Access Key is not defined.");
        return this.defaultImage; // Fallback image
      }

      const unsplashUrl = `https://api.unsplash.com/search/photos?query=${encodeURIComponent(
        query
      )}&client_id=${unsplashAccessKey}&per_page=1&orientation=landscape`;

      try {
        const response = await axios.get(unsplashUrl);
        console.log(`Unsplash API Response for "${query}":`, response.data);

        if (
          response.data &&
          response.data.results &&
          response.data.results.length > 0
        ) {
          return response.data.results[0].urls.regular;
        } else {
          console.warn(`No Unsplash images found for query: "${query}"`);
          return this.defaultImage; // Fallback image
        }
      } catch (error) {
        console.error(
          `Error fetching image from Unsplash for query "${query}":`,
          error.message
        );
        return this.defaultImage; // Fallback image
      }
    },

    toggleSortOrder() {
      this.sortCriteria.direction = this.sortCriteria.direction === 'desc' ? 'asc' : 'desc';
    },

    updateSortCriteria(event) {
      const value = event.target.value;
      const [field, direction] = value.split('-');
      this.sortCriteria.field = field;
      this.sortCriteria.direction = direction;
    },

    async fetchAttractions() {
      const countryRef = doc(db, "countries", this.country);
      try {
        console.log(`Fetching attractions for ${this.country} from Firestore...`);
        const countryDoc = await getDoc(countryRef);
        if (countryDoc.exists()) {
          console.log(`Fetched attractions from Firestore for ${this.country}`);
          this.attractions = countryDoc.data().attractions;
          this.loading = false;
        } else {
          const cities = this.getCountryCities(this.country);
          console.log(`No attractions in Firestore for ${this.country}, fetching from API...`)
          if (cities.length === 0) {
            this.errorMessage = "No cities available for the selected country.";
            this.loading = false;
            return;
          }

          let allAttractions = [];
          const radius = this.countryRadius[this.country] || this.defaultRadius;
          console.log(`Using radius: ${radius} meters for country: ${this.country}`);

          for (const city of cities) {
            const { name, location } = city;
            // **Determine the Radius: City-specific > Country-specific > Default**
            const citySpecificRadius = this.cityRadius[name];
            const radius = citySpecificRadius || this.countryRadius[this.country] || this.defaultRadius;
            console.log(`Using radius: ${radius} meters for city: ${name} in country: ${this.country}`);

            const type = "tourist_attraction";
            const proxyUrl = `/api/place/nearbysearch/json?location=${location}&radius=${radius}&type=${type}&key=${this.apiKey}`;

            try {
              const response = await axios.get(proxyUrl);
              if (response.data.status !== "OK") {
                console.error(`Error fetching attractions for ${name}:`, response.data.status, response.data.error_message || "");
                continue;
              }

              const mappedAttractions = response.data.results.map((place) => ({
                name: place.name,
                place_id: place.place_id,
                vicinity: place.vicinity,
                image: place.photos
                  ? `https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${place.photos[0].photo_reference}&key=${this.apiKey}`
                  : null,
                coordinates: place.geometry?.location || { lat: 0, lng: 0 },
                rating: place.rating || 0,
                user_ratings_total: place.user_ratings_total || 0,
                open_now: place.opening_hours?.open_now || false,
                city: name,
              }));

              allAttractions = allAttractions.concat(mappedAttractions);
            } catch (apiError) {
              console.error(`Error fetching attractions for ${name}:`, apiError.message);
              continue;
            }
          }

          if (allAttractions.length === 0) {
            this.errorMessage = "No attractions found for the selected country.";
            this.loading = false;
            return;
          }

          const uniqueAttractions = Array.from(new Map(allAttractions.map(item => [item.place_id, item])).values());
          const topAttractions = uniqueAttractions.slice(0, 50);

          // Fetch Unsplash images for attractions missing Google images
          const fetchImagesPromises = topAttractions.map(async (attraction) => {
            if (!attraction.image) {

              const query = `${attraction.name}, ${attraction.city}`;
              console.log(`Fetching Unsplash image for: ${query}`); // Debugging log
              const unsplashImage = await this.getUnsplashImage(query);
              console.log(`Fetched image URL: ${unsplashImage}`); // Debugging log
              attraction.image = unsplashImage;
            }
          });

          await Promise.all(fetchImagesPromises);

          // Assign fallback image if still null
          topAttractions.forEach(place => {
            if (!place.image) {
              place.image = this.defaultImage; // Ensure this path is correct
            }
          });

          this.attractions = topAttractions;

          await setDoc(countryRef, {
            attractions: this.attractions,
            lastUpdated: new Date(),
          });

          this.loading = false;
        }
      } catch (error) {
        console.error("Error accessing Firestore:", error);
        this.errorMessage = "Failed to access the database. Please try again later.";
        this.loading = false;
      }
    },


    getCountryCities(country) {
      const cities = {
        France: [
          { name: "Paris", location: "48.8566,2.3522" },
          { name: "Lyon", location: "45.7640,4.8357" },
          { name: "Marseille", location: "43.2965,5.3698" },
          { name: "Nice", location: "43.7102,7.2620" },
          { name: "Bordeaux", location: "44.8378,-0.5792" },
        ],
        Italy: [
          { name: "Rome", location: "41.9028,12.4964" },
          { name: "Milan", location: "45.4642,9.1900" },
          { name: "Venice", location: "45.4408,12.3155" },
          { name: "Florence", location: "43.7696,11.2558" },
          { name: "Naples", location: "40.8518,14.2681" },
        ],
        Japan: [
          { name: "Tokyo", location: "35.6895,139.6917" },
          { name: "Kyoto", location: "35.0116,135.7681" },
          { name: "Osaka", location: "34.6937,135.5023" },
          { name: "Sapporo", location: "43.0618,141.3545" },
          { name: "Nagoya", location: "35.1815,136.9066" },
        ],
        "United States": [
          { name: "New York City", location: "40.7128,-74.0060" },
          { name: "Los Angeles", location: "34.0522,-118.2437" },
          { name: "Chicago", location: "41.8781,-87.6298" },
          { name: "Las Vegas", location: "36.1699,-115.1398" },
          { name: "Miami", location: "25.7617,-80.1918" },
        ],
        Spain: [
          { name: "Madrid", location: "40.4168,-3.7038" },
          { name: "Barcelona", location: "41.3851,2.1734" },
          { name: "Seville", location: "37.3891,-5.9845" },
          { name: "Valencia", location: "39.4699,-0.3763" },
          { name: "Granada", location: "37.1773,-3.5986" },
        ],
        China: [
          { name: "Beijing", location: "39.9042,116.4074" },
          { name: "Shanghai", location: "31.2304,121.4737" },
          { name: "Guangzhou", location: "23.1291,113.2644" },
          { name: "Shenzhen", location: "22.5431,114.0579" },
          { name: "Chengdu", location: "30.5728,104.0668" },
        ],
        Mexico: [
          { name: "Mexico City", location: "19.4326,-99.1332" },
          { name: "Guadalajara", location: "20.6597,-103.3496" },
          { name: "Monterrey", location: "25.6866,-100.3161" },
          { name: "Cancun", location: "21.1619,-86.8515" },
          { name: "Puebla", location: "19.0413,-98.2062" },
        ],
        "United Kingdom": [
          { name: "London", location: "51.5074,-0.1278" },
          { name: "Edinburgh", location: "55.9533,-3.1883" },
          { name: "Manchester", location: "53.4808,-2.2426" },
          { name: "Birmingham", location: "52.4862,-1.8904" },
          { name: "Glasgow", location: "55.8642,-4.2518" },
        ],
        Germany: [
          { name: "Berlin", location: "52.5200,13.4050" },
          { name: "Munich", location: "48.1351,11.5820" },
          { name: "Frankfurt", location: "50.1109,8.6821" },
          { name: "Hamburg", location: "53.5511,9.9937" },
          { name: "Cologne", location: "50.9375,6.9603" },
        ],
        Thailand: [
          { name: "Bangkok", location: "13.7563,100.5018" },
          { name: "Chiang Mai", location: "18.7883,98.9853" },
          { name: "Phuket", location: "7.8804,98.3923" },
          { name: "Pattaya", location: "12.9236,100.8825" },
          { name: "Ayutthaya", location: "14.3532,100.5683" },
        ],
        Turkey: [
          { name: "Istanbul", location: "41.0082,28.9784" },
          { name: "Ankara", location: "39.9334,32.8597" },
          { name: "Izmir", location: "38.4237,27.1428" },
          { name: "Antalya", location: "36.8841,30.7056" },
          { name: "Bursa", location: "40.1950,29.0600" },
        ],
        Australia: [
          { name: "Sydney", location: "-33.8688,151.2093" },
          { name: "Melbourne", location: "-37.8136,144.9631" },
          { name: "Brisbane", location: "-27.4698,153.0251" },
          { name: "Perth", location: "-31.9505,115.8605" },
          { name: "Adelaide", location: "-34.9285,138.6007" },
        ],
        Brazil: [
          { name: "Rio de Janeiro", location: "-22.9068,-43.1729" },
          { name: "Sao Paulo", location: "-23.5505,-46.6333" },
          { name: "Brasilia", location: "-15.7942,-47.8822" },
          { name: "Salvador", location: "-12.9777,-38.5016" },
          { name: "Fortaleza", location: "-3.7319,-38.5267" },
        ],
        Canada: [
          { name: "Toronto", location: "43.6532,-79.3832" },
          { name: "Vancouver", location: "49.2827,-123.1207" },
          { name: "Montreal", location: "45.5017,-73.5673" },
          { name: "Calgary", location: "51.0447,-114.0719" },
          { name: "Ottawa", location: "45.4215,-75.6972" },
        ],
        India: [
          { name: "New Delhi", location: "28.6139,77.2090" },
          { name: "Mumbai", location: "19.0760,72.8777" },
          { name: "Bangalore", location: "12.9716,77.5946" },
          { name: "Chennai", location: "13.0827,80.2707" },
          { name: "Kolkata", location: "22.5726,88.3639" },
        ],
        "South Africa": [
          { name: "Johannesburg", location: "-26.2041,28.0473" },
          { name: "Cape Town", location: "-33.9249,18.4241" },
          { name: "Durban", location: "-29.8587,31.0218" },
          { name: "Pretoria", location: "-25.7479,28.2293" },
          { name: "Port Elizabeth", location: "-33.9608,25.6022" },
        ],
        Russia: [
          { name: "Moscow", location: "55.7558,37.6176" },
          { name: "Saint Petersburg", location: "59.9343,30.3351" },
          { name: "Novosibirsk", location: "55.0084,82.9357" },
          { name: "Yekaterinburg", location: "56.8389,60.6057" },
          { name: "Kazan", location: "55.8304,49.0661" },
        ],
        Argentina: [
          { name: "Buenos Aires", location: "-34.6037,-58.3816" },
          { name: "Cordoba", location: "-31.4201,-64.1888" },
          { name: "Rosario", location: "-32.9468,-60.6393" },
          { name: "Mendoza", location: "-32.8895,-68.8458" },
          { name: "La Plata", location: "-34.9205,-57.9545" },
        ],
        Netherlands: [
          { name: "Amsterdam", location: "52.3676,4.9041" },
          { name: "Rotterdam", location: "51.9244,4.4777" },
          { name: "The Hague", location: "52.0705,4.3007" },
          { name: "Utrecht", location: "52.0907,5.1214" },
          { name: "Eindhoven", location: "51.4416,5.4697" },
        ],
        Greece: [
          { name: "Athens", location: "37.9838,23.7275" },
          { name: "Thessaloniki", location: "40.6401,22.9444" },
          { name: "Patras", location: "38.2466,21.7346" },
          { name: "Heraklion", location: "35.3387,25.1442" },
          { name: "Larissa", location: "39.6390,22.4194" },
        ],
        Malaysia: [
          { name: "Kuala Lumpur", location: "3.1390,101.6869" },
          { name: "George Town", location: "5.4141,100.3288" },
          { name: "Johor Bahru", location: "1.4927,103.7414" },
          { name: "Kota Kinabalu", location: "5.9804,116.0735" },
          { name: "Malacca City", location: "2.1896,102.2501" },
        ],
        Egypt: [
          { name: "Cairo", location: "30.0444,31.2357" },
          { name: "Alexandria", location: "31.2001,29.9187" },
          { name: "Giza", location: "30.0131,31.2089" },
          { name: "Luxor", location: "25.6872,32.6396" },
          { name: "Aswan", location: "24.0889,32.8998" },
        ],
        Switzerland: [
          { name: "Zurich", location: "47.3769,8.5417" },
          { name: "Geneva", location: "46.2044,6.1432" },
          { name: "Basel", location: "47.5596,7.5886" },
          { name: "Bern", location: "46.8182,8.2275" },
          { name: "Lausanne", location: "46.5197,6.6323" },
        ],
        Indonesia: [
          { name: "Jakarta", location: "-6.2088,106.8456" },
          { name: "Bali (Denpasar)", location: "-8.6500,115.2167" },
          { name: "Surabaya", location: "-7.2575,112.7521" },
          { name: "Bandung", location: "-6.9175,107.6191" },
          { name: "Yogyakarta", location: "-7.7956,110.3695" },
        ],
        Portugal: [
          { name: "Lisbon", location: "38.7223,-9.1393" },
          { name: "Porto", location: "41.1579,-8.6291" },
          { name: "Faro", location: "37.0194,-7.9304" },
          { name: "Coimbra", location: "40.2033,-8.4103" },
          { name: "Braga", location: "41.5453,-8.4265" },
        ],
        Austria: [
          { name: "Vienna", location: "48.2082,16.3738" },
          { name: "Salzburg", location: "47.8095,13.0550" },
          { name: "Innsbruck", location: "47.2692,11.4041" },
          { name: "Graz", location: "47.0707,15.4395" },
          { name: "Linz", location: "48.3069,14.2858" },
        ],
        Sweden: [
          { name: "Stockholm", location: "59.3293,18.0686" },
          { name: "Gothenburg", location: "57.7089,11.9746" },
          { name: "Malmö", location: "55.604981,13.003822" },
          { name: "Uppsala", location: "59.8586,17.6389" },
          { name: "Västerås", location: "59.6168,16.5528" },
        ],
        Vietnam: [
          { name: "Hanoi", location: "21.0285,105.8542" },
          { name: "Ho Chi Minh City", location: "10.8231,106.6297" },
          { name: "Da Nang", location: "16.0544,108.2022" },
          { name: "Hue", location: "16.4637,107.5908" },
          { name: "Nha Trang", location: "12.2388,109.1967" },
        ],
        Singapore: [{ name: "Singapore", location: "1.3521,103.8198" }],
        "New Zealand": [
          { name: "Auckland", location: "-36.8485,174.7633" },
          { name: "Wellington", location: "-41.2865,174.7762" },
          { name: "Christchurch", location: "-43.5321,172.6362" },
          { name: "Hamilton", location: "-37.7870,175.2793" },
          { name: "Dunedin", location: "-45.8788,170.5028" },
        ],
        Poland: [
          { name: "Warsaw", location: "52.2297,21.0122" },
          { name: "Krakow", location: "50.0647,19.9450" },
          { name: "Gdansk", location: "54.3520,18.6466" },
          { name: "Wroclaw", location: "51.1079,17.0385" },
          { name: "Poznan", location: "52.4064,16.9252" },
        ],
        Morocco: [
          { name: "Casablanca", location: "33.5731,-7.5898" },
          { name: "Marrakesh", location: "31.6295,-7.9811" },
          { name: "Rabat", location: "34.0209,-6.8416" },
          { name: "Fez", location: "34.0181,-5.0064" },
          { name: "Tangier", location: "35.7595,-5.8339" },
        ],
        Philippines: [
          { name: "Manila", location: "14.5995,120.9842" },
          { name: "Cebu City", location: "10.3157,123.8854" },
          { name: "Davao City", location: "7.1907,125.4553" },
          { name: "Baguio", location: "16.4023,120.5960" },
          { name: "Iloilo City", location: "10.7201,122.5621" },
        ],
        Chile: [
          { name: "Santiago", location: "-33.4489,-70.6693" },
          { name: "Valparaiso", location: "-33.0472,-71.6127" },
          { name: "Concepcion", location: "-36.8201,-73.0444" },
          { name: "La Serena", location: "-29.9045,-71.2451" },
          { name: "Antofagasta", location: "-23.6505,-70.3975" },
        ],
        "South Korea": [
          { name: "Seoul", location: "37.5665,126.9780" },
          { name: "Busan", location: "35.1796,129.0756" },
          { name: "Incheon", location: "37.4563,126.7052" },
          { name: "Daegu", location: "35.8722,128.6025" },
          { name: "Daejeon", location: "36.3504,127.3845" },
        ],
        "United Arab Emirates": [
          { name: "Dubai", location: "25.276987,55.296249" },
          { name: "Abu Dhabi", location: "24.4539,54.3773" },
          { name: "Sharjah", location: "25.3463,55.4209" },
          { name: "Al Ain", location: "24.2074,55.7608" },
          { name: "Ras Al Khaimah", location: "25.8000,55.9833" },
        ],
        "Czech Republic": [
          { name: "Prague", location: "50.0755,14.4378" },
          { name: "Brno", location: "49.1951,16.6068" },
          { name: "Ostrava", location: "49.8209,18.2625" },
          { name: "Plzen", location: "49.7475,13.3771" },
          { name: "Liberec", location: "50.7670,15.0562" },
        ],
        "Saudi Arabia": [
          { name: "Riyadh", location: "24.7136,46.6753" },
          { name: "Jeddah", location: "21.4858,39.1925" },
          { name: "Mecca", location: "21.3891,39.8579" },
          { name: "Medina", location: "24.5247,39.5692" },
          { name: "Dammam", location: "26.3927,50.0888" },
        ],
        Belgium: [
          { name: "Brussels", location: "50.8503,4.3517" },
          { name: "Antwerp", location: "51.2194,4.4025" },
          { name: "Ghent", location: "51.0543,3.7174" },
          { name: "Bruges", location: "51.2093,3.2247" },
          { name: "Leuven", location: "50.8798,4.7005" },
        ],
        Israel: [
          { name: "Jerusalem", location: "31.7683,35.2137" },
          { name: "Tel Aviv", location: "32.0853,34.7818" },
          { name: "Haifa", location: "32.7940,34.9896" },
          { name: "Eilat", location: "29.5581,34.9482" },
          { name: "Beersheba", location: "31.2518,34.7913" },
        ],
        Peru: [
          { name: "Lima", location: "-12.0464,-77.0428" },
          { name: "Cusco", location: "-13.5319,-71.9675" },
          { name: "Arequipa", location: "-16.4090,-71.5375" },
          { name: "Trujillo", location: "-8.1164,-79.0283" },
          { name: "Chiclayo", location: "-6.7764,-79.8403" },
        ],
        Norway: [
          { name: "Oslo", location: "59.9139,10.7522" },
          { name: "Bergen", location: "60.3913,5.3221" },
          { name: "Trondheim", location: "63.4305,10.3951" },
          { name: "Stavanger", location: "58.9690,5.7331" },
          { name: "Tromsø", location: "69.6492,18.9560" },
        ],
        Denmark: [
          { name: "Copenhagen", location: "55.6761,12.5683" },
          { name: "Aarhus", location: "56.1629,10.2039" },
          { name: "Odense", location: "55.4038,10.4024" },
          { name: "Aalborg", location: "57.0467,9.9187" },
          { name: "Esbjerg", location: "55.4765,8.4594" },
        ],
        Hungary: [
          { name: "Budapest", location: "47.4979,19.0402" },
          { name: "Debrecen", location: "47.5316,21.6273" },
          { name: "Szeged", location: "46.2530,20.1414" },
          { name: "Miskolc", location: "48.1039,20.7944" },
          { name: "Pécs", location: "46.0727,18.2323" },
        ],
        Ireland: [
          { name: "Dublin", location: "53.3498,-6.2603" },
          { name: "Cork", location: "51.8985,-8.4756" },
          { name: "Galway", location: "53.2707,-9.0568" },
          { name: "Limerick", location: "52.6638,-8.6267" },
          { name: "Waterford", location: "52.2593,-7.1100" },
        ],
        Finland: [
          { name: "Helsinki", location: "60.1695,24.9354" },
          { name: "Espoo", location: "60.2055,24.6559" },
          { name: "Tampere", location: "61.4978,23.7610" },
          { name: "Vantaa", location: "60.2934,25.0403" },
          { name: "Oulu", location: "65.0121,25.4682" },
        ],
        Colombia: [
          { name: "Bogotá", location: "4.7110,-74.0721" },
          { name: "Medellín", location: "6.2442,-75.5812" },
          { name: "Cali", location: "3.4516,-76.5319" },
          { name: "Cartagena", location: "10.3910,-75.4794" },
          { name: "Barranquilla", location: "10.9685,-74.7813" },
        ],
        Ukraine: [
          { name: "Kyiv", location: "50.4501,30.5234" },
          { name: "Lviv", location: "49.8397,24.0297" },
          { name: "Odessa", location: "46.4825,30.7233" },
          { name: "Kharkiv", location: "49.9935,36.2304" },
          { name: "Dnipro", location: "48.4647,35.0462" },
        ],
      };
      return cities[country] || [];
    },
    getContinent(country) {
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
      return continentMapping[country] || 'Unknown';
    },

    goBack() {
      this.$router.go(-1);
    },

    showSavedPopup() {
      this.toastMessage = "Added to Saved Places!";
      this.toastType = "add"; // Use 'add' type for success
      this.toastShow = true; // Show the toast
    },

    displayAlreadySavedPopup() {
      this.toastMessage = "Place has already been saved!";
      this.toastType = "info"; // Use 'info' type for already saved
      this.toastShow = true; // Show the toast
    },

    isPlaceSaved(placeId) {
      // Check if the place is already saved using the reactive state
      if (
        this.savedPlacesState &&
        Array.isArray(this.savedPlacesState.savedPlaces)
      ) {
        return this.savedPlaceIds.has(placeId); // Using computed property for efficiency
      }
      return false;
    },
    async savePlaceToFirebase(placeId) {
      const user = auth.currentUser;

      if (user) {
        this.userId = user.uid; // Ensure this is set

        const attraction = this.attractions.find(
          (attraction) => attraction.place_id === placeId
        );

        if (attraction) {
          const placeData = {
            place_id: attraction.place_id || null,
            name: attraction.name || "Unknown",
            vicinity: attraction.vicinity || "Unknown vicinity",
            image: attraction.image || "/default-image.jpg",
            coordinates: attraction.coordinates,
            rating: attraction.rating || 0,
            user_ratings_total: attraction.user_ratings_total || 0,
            open_now: attraction.open_now || false,
            city: attraction.city || "Unknown City",
            country: this.country || "Unknown Country",
            source: "google_places",
            summary: "Google Places Summary",
            activities: [],
            timestamp: new Date(),
          };

          try {
            // Use the global state to add the place
            const wasAdded = await this.savedPlacesState.addPlace(this.userId, placeData);
            console.log(`Was the place added? ${wasAdded}`);
            if (wasAdded) {
              this.showSavedPopup();
            } else {
              this.displayAlreadySavedPopup();
            }
          } catch (error) {
            console.error("Error saving place to Firebase:", error);
            this.errorMessage = "Failed to save the place. Please try again.";
          }
        } else {
          console.error("Attraction not found for saving.");
          this.errorMessage = "Attraction data is missing. Unable to save.";
        }
      } else {
        console.error("User is not authenticated");
        this.errorMessage = "You must be logged in to save places.";
      }
    },

    async generateItinerary() {
      // Implement your itinerary generation logic here
      console.log("Generate Itinerary button clicked");
      // This could involve creating a new itinerary document in Firestore
    },


  },
  mounted() {
    // Listen for authentication state changes
    auth.onAuthStateChanged((user) => {
      if (user) {
        this.userId = user.uid;
        // Load saved places for the authenticated user
        if (
          this.savedPlacesState &&
          typeof this.savedPlacesState.loadSavedPlaces === "function"
        ) {
          this.savedPlacesState.loadSavedPlaces(user.uid);
        }
      } else {
        console.error("User is not authenticated");
        this.userId = null;
        // Clear the global savedPlacesState
        if (
          this.savedPlacesState &&
          typeof this.savedPlacesState.clearSavedPlaces === "function"
        ) {
          this.savedPlacesState.clearSavedPlaces();
        }
      }
    });
  },
};
</script>

<style scoped>
/* <====================== secondary header ===================> */
.secondary_header {
  position: relative;
  padding: 1rem 0;
  margin-top: 2.4rem;
  /* Add spacing above the header */
  margin-bottom: 4rem;
  /* Add spacing below the header */
  text-align: left;
  /* Center align the text */
}

.secondary_content {
  padding: 0 60px;
}

.secondary_content h5 {
  color: rgb(166, 163, 163);
  margin-bottom: 1rem;
}

/* Container to align dropdowns side by side */
.dropdown-container {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  margin-left: 60px;
  /* Adjust this value to align the dropdowns with the text */
  z-index: 100;
  /* Ensure it's above other page content */
}

/* Style the dropdown button */
.dropdown-btn {
  background-color: #222;
  /* Dark background color */
  color: #fff;
  /* White text */
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  transition: background-color 0.3s ease;
  padding: 16px;
}

/* Change button color on hover */
.dropdown-btn:hover {
  background-color: #555;
}

/* Dropdown content styling */
.dropdown-content {
  opacity: 0;
  visibility: hidden;
  position: absolute;
  background-color: #222;
  min-width: 200px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  border-radius: 5px;
  z-index: 9999;
  top: 100%;
  left: 0;
  padding: 10px 0;
  transition: opacity 0.3s ease, transform 0.5s ease;
  transform: translateY(-10px);
}

.dropdown:hover .dropdown-content {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

/* Dropdown content links */
.dropdown-content a {
  color: white;
  padding: 10px 20px;
  text-decoration: none;
  display: block;
  transition: background-color 0.3s ease;
}

/* Change background color on hover */
.dropdown-content a:hover {
  background-color: #333;
}

/* Show dropdown on hover */
.dropdown:hover .dropdown-content {
  display: block;
}


/* <================== layout ================>*/
.destination-details {
  text-align: center;
  font-family: "Source Sans 3", sans-serif;
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 5%;
  position: relative;
}

.back-button {
  background-color: black;
  color: white;
  border: 1px solid black;
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.back-button:hover {
  transform: scale(1.05);
  background-color: black;
  color: white;
}

.page-title {
  font-size: 2rem;
  /* Adjusted font size */
  color: black;
  font-weight: bolder;
  flex-grow: 1;
}

.filter-dropdown {
  margin: 10px 0;
  font-family: "Source Sans 3", sans-serif;
}

.filter-dropdown .form-select {
  width: 350px;
  border-radius: 0.5rem;
  border: 1px solid black;
  font-family: "Source Sans 3", sans-serif;
  padding: 8px;
  font-size: 1rem;
  background-color: white;
  color: black;
  cursor: pointer;
}

.filter-dropdown .form-select:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 5px rgba(52, 152, 219, 0.5);
}

.loading {
  font-size: 1.5rem;
  margin: 50px;
  color: black;
}

.error-message {
  color: red;
  margin: 20px;
  font-size: 1rem;
}

/* Card Grid Layout */
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  /* 3 items per row on large screens */
  gap: 1.5rem;
  /* Space between cards */
  padding: 2rem;
  /* Padding around the grid */
}

.card-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  overflow: hidden;
  border-radius: 1.5rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  background: rgba(0, 0, 0, 0.0);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-container:hover {
  transform: translateY(-4px);
  /* Slightly lifts the card on hover */
  box-shadow: 0 8px 24px hsla(0, 0%, 0%, 0.2);
  /* Enhances shadow for lift effect */
}

.destination-card {
  position: relative;
  /* To position overlay and buttons */
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  width: 100%;
  height: 400px;
  /* Adjust height as needed */
  background-size: cover;
  background-position: center;
  border-radius: inherit;
  padding: 1.5rem;
  box-sizing: border-box;
  color: #ffffff;
  /* Text color for readability on image */
  overflow: hidden;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  /* Slightly opaque black background */
  z-index: 1;
  /* Place between background image and text */
  border-radius: inherit;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 15px;
  background: transparent;
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  z-index: 2;
}

.close-button:hover {
  color: red;
}

.card-body {
  position: absolute;
  /* Position absolutely within the card */
  bottom: 15px;
  /* Align to the bottom with some padding */
  left: 15px;
  /* Align to the left with some padding */
  z-index: 2;
  /* Ensure it stays above the overlay */
  text-align: left;
  /* Align text to the left */
  width: calc(100% - 30px);
  /* Prevent overflow */
}


.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  margin: 0;
  /* Remove any extra margins */
  padding: 0;
}

.card-text {
  font-size: 0.9rem;
  color: #eaeaea;
  margin-top: 0.1rem;
  /* Adjust spacing if needed */
  margin-bottom: 0;
  margin-left: 0;
  padding: 0;
}

.rating-section {
  display: flex;
  align-items: center;
  margin-top: 0;
  padding: 0;
}

.rating-number {
  margin-left: 8px;
  font-size: 0.9rem;
  color: #ffffff;
}

.rating-text {
  margin-left: 0;
  font-size: 0.9rem;
  color: #ffffff;
}


.itinerary-button {
  margin-top: 10px;
  background-color: black;
  color: white;
  padding: 8px;
  font-size: 0.8rem;
  font-weight: bold;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
  opacity: 1;
}

.itinerary-button:hover {
  background-color: #333;
  color: white;
}

.itinerary-button.saved {
  opacity: 0.7;
  /* Reduced opacity when saved */
}

/* Responsive adjustments */
@media (max-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
    /* 2 items per row on medium screens */
  }
}

@media (max-width: 768px) {
  .card-grid {
    grid-template-columns: 1fr;
    /* 1 item per row on small screens */
  }
  
  .dropdown-container {
        flex-direction: column;
        /* Stack buttons vertically */
        align-items: flex-start;
        /* Align them to the start */
        gap: 0.5rem;
        /* Adjust gap for vertical spacing */
    }
}

.transition-wrapper {
  display: contents;
  /* Keep the child elements visible */
  flex-wrap: wrap;
  justify-content: flex-start;
  gap: 15px;
  padding: 20px;
}


.already-saved {
  background-color: #e74c3c;
  /* Different color for already saved */
}

/* Additional Styles for Dropdown (already provided by user) */
.btn {
  font-family: "Source Sans 3", sans-serif;
}


</style>
