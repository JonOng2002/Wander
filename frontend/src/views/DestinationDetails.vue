<template>
  <div class="destination-details">
    <div class="header-row">
      <button @click="goBack" class="btn back-button">Back to Destinations</button>
      <h1 class="page-title">Top Tourist Attractions in {{ country }}</h1>
    </div>

    <!-- Display Loading Indicator -->
    <div v-if="loading" class="loading">Loading...</div>

    <!-- Display Error Message -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <!-- Display Attractions List -->
    <div v-if="!loading && !errorMessage" class="attractions-list">
      <div
        v-for="attraction in attractions"
        :key="attraction.place_id"
        class="attraction-card"
      >
        <img
          :src="attraction.image"
          alt="attraction-image"
          class="attraction-image"
          loading="lazy"
        />
        <h2 class="attraction-name">{{ attraction.name }}</h2>
        <p class="attraction-vicinity">{{ attraction.vicinity }}</p>

        <!-- Display Rating and Number of Reviews -->
        <p v-if="attraction.rating !== 0" class="attraction-rating">
          ⭐ {{ attraction.rating }} ({{ attraction.user_ratings_total }} reviews)
        </p>
        <p v-else class="attraction-rating">No ratings available</p>

        <!-- Display Open Status -->
        <p v-if="attraction.open_now !== undefined" class="attraction-hours">
          {{ attraction.open_now ? '🟢 Open Now' : '🔴 Closed' }}
        </p>

        <save-place-button
          class="btn save-button"
          :placeId="attraction.place_id || `manual-${Date.now()}`"
          :placeName="attraction.name"
          :vicinity="attraction.vicinity || 'Unknown vicinity'"
          :country="country"
          :city="attraction.city || 'Unknown City'"
          :latitude="attraction.coordinates?.lat ?? 0"
          :longitude="attraction.coordinates?.lng ?? 0"
          :placePng="attraction.image || '/default-image.jpg'"
          :userId="userId"
          :summary="'Google Places Summary'"
          :source="'google_places'"
          :activities="[]"
          @place-saved="handlePlaceSaved(attraction.place_id)"
        >
          Add to Saved Places
        </save-place-button>
      </div>
    </div>

    <!-- Popup Notification -->
    <div v-if="showPopup" class="popup">
      <p>Added to saved places!</p>
    </div>

    <!-- Display Saved Places -->
    <div class="saved-places-list" v-if="savedPlacesState.savedPlaces.length > 0">
      <h2>Your Saved Places</h2>
      <ul>
        <li
          v-for="(place, index) in savedPlacesState.savedPlaces"
          :key="index"
        >
          {{ place.name }} - {{ place.vicinity }}
        </li>
      </ul>
      <button @click="generateItinerary" class="btn generate-btn">
        Generate Itinerary!
      </button>
    </div>
  </div>
</template>

<script>
// Import necessary components and functions
import SavePlaceButton from "@/components/SavePlaceButton.vue"; // Adjust the path as needed
import { auth, db } from '@/main.js'; // Adjust the path based on your project structure
import { doc, getDoc, setDoc, arrayUnion } from "firebase/firestore"; // Removed arrayRemove
import axios from "axios";

export default {
  name: "DestinationDetails",
  components: {
    SavePlaceButton,
  },
  inject: ['savedPlacesState'], // Inject the provided global state
  data() {
    return {
      attractions: [],
      loading: true,
      country: this.$route.params.country,
      // Your Google Places API Key
      apiKey: 'API_KEY_HERE',
      cityName: this.$route.params.city || 'Unknown City',
      userId: null,
      showPopup: false,
      currentAttractionId: null, // Defined to track the current attraction ID
      errorMessage: '', // For user-friendly error messages
    };
  },
  created() {
    this.fetchAttractions();
  },
  methods: {
    handlePlaceSaved(placeId) {
      this.currentAttractionId = placeId; // Set the current attraction ID
      this.showSavedPopup(); // Show the popup

      // Save the place to the user's saved places
      this.savePlaceToFirebase(placeId);
    },
    async fetchAttractions() {
      const countryRef = doc(db, "countries", this.country);
      try {
        // Check if attractions for the country exist in Firestore
        const countryDoc = await getDoc(countryRef);
        if (countryDoc.exists()) {
          // Attractions exist, use them
          console.log(`Fetched attractions for ${this.country} from Firestore.`);
          this.attractions = countryDoc.data().attractions;
          this.loading = false;
        } else {
          // Attractions do not exist, fetch from Google Places API via proxy
          console.log(`No data for ${this.country} in Firestore. Fetching from Google API via proxy.`);
          const cities = this.getCountryCities(this.country);
          if (cities.length === 0) {
            console.error(`No cities found for ${this.country}`);
            this.errorMessage = 'No cities available for the selected country.';
            this.loading = false;
            return;
          }

          let allAttractions = [];

          // Fetch attractions for each city
          for (const city of cities) {
            const { name, location } = city;
            const radius = 50000; // 50 km
            const type = "tourist_attraction";
            const proxyUrl = `/api/place/nearbysearch/json?location=${location}&radius=${radius}&type=${type}&key=${this.apiKey}`;

            try {
              const response = await axios.get(proxyUrl);
              if (response.data.error) {
                console.error(`Error fetching attractions for ${name}:`, response.data.error);
                continue; // Skip to the next city on error
              }
              console.log(`Fetched attractions for ${name}:`, response.data.results);

              // Map attractions with additional data
              const mappedAttractions = response.data.results.map((place) => ({
                name: place.name,
                place_id: place.place_id,
                vicinity: place.vicinity,
                image: place.photos
                  ? `https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${place.photos[0].photo_reference}&key=${this.apiKey}`
                  : "/default-image.jpg",
                coordinates: place.geometry?.location || { lat: 0, lng: 0 },
                rating: place.rating || 0,
                user_ratings_total: place.user_ratings_total || 0,
                open_now: place.opening_hours?.open_now || false,
                city: name, // Add city name to attraction
              }));

              allAttractions = allAttractions.concat(mappedAttractions);
            } catch (apiError) {
              console.error(`Error fetching attractions for ${name}:`, apiError);
              continue; // Skip to the next city on error
            }
          }

          if (allAttractions.length === 0) {
            this.errorMessage = 'No attractions found for the selected country.';
            this.loading = false;
            return;
          }

          // Remove duplicate attractions based on place_id
          const uniqueAttractions = Array.from(
            new Map(allAttractions.map((item) => [item.place_id, item])).values()
          );

          // Sort attractions by rating and number of user ratings
          uniqueAttractions.sort((a, b) => {
            if (b.rating !== a.rating) {
              return b.rating - a.rating;
            }
            return b.user_ratings_total - a.user_ratings_total;
          });

          // Limit to top 20 attractions
          this.attractions = uniqueAttractions.slice(0, 20);

          // Save the attractions to Firestore
          await setDoc(countryRef, {
            attractions: this.attractions,
            lastUpdated: new Date(),
          });

          console.log(`Saved attractions for ${this.country} to Firestore.`);
          this.loading = false;
        }
      } catch (error) {
        console.error("Error accessing Firestore:", error);
        this.errorMessage = 'Failed to access the database. Please try again later.';
        this.loading = false;
      }
    },
    getCountryCities(country) {
      const cities = {
        'France': [
          { name: 'Paris', location: '48.8566,2.3522' },
          { name: 'Lyon', location: '45.7640,4.8357' },
          { name: 'Marseille', location: '43.2965,5.3698' },
          { name: 'Nice', location: '43.7102,7.2620' },
          { name: 'Bordeaux', location: '44.8378,-0.5792' },
        ],
        'Italy': [
          { name: 'Rome', location: '41.9028,12.4964' },
          { name: 'Milan', location: '45.4642,9.1900' },
          { name: 'Venice', location: '45.4408,12.3155' },
          { name: 'Florence', location: '43.7696,11.2558' },
          { name: 'Naples', location: '40.8518,14.2681' },
        ],
        'Japan': [
          { name: 'Tokyo', location: '35.6895,139.6917' },
          { name: 'Kyoto', location: '35.0116,135.7681' },
          { name: 'Osaka', location: '34.6937,135.5023' },
          { name: 'Sapporo', location: '43.0618,141.3545' },
          { name: 'Nagoya', location: '35.1815,136.9066' },
        ],
        'United States': [
          { name: 'New York City', location: '40.7128,-74.0060' },
          { name: 'Los Angeles', location: '34.0522,-118.2437' },
          { name: 'Chicago', location: '41.8781,-87.6298' },
          { name: 'Las Vegas', location: '36.1699,-115.1398' },
          { name: 'Miami', location: '25.7617,-80.1918' },
        ],
        'Spain': [
          { name: 'Madrid', location: '40.4168,-3.7038' },
          { name: 'Barcelona', location: '41.3851,2.1734' },
          { name: 'Seville', location: '37.3891,-5.9845' },
          { name: 'Valencia', location: '39.4699,-0.3763' },
          { name: 'Granada', location: '37.1773,-3.5986' },
        ],
        'China': [
          { name: 'Beijing', location: '39.9042,116.4074' },
          { name: 'Shanghai', location: '31.2304,121.4737' },
          { name: 'Guangzhou', location: '23.1291,113.2644' },
          { name: 'Shenzhen', location: '22.5431,114.0579' },
          { name: 'Chengdu', location: '30.5728,104.0668' },
        ],
        'Mexico': [
          { name: 'Mexico City', location: '19.4326,-99.1332' },
          { name: 'Guadalajara', location: '20.6597,-103.3496' },
          { name: 'Monterrey', location: '25.6866,-100.3161' },
          { name: 'Cancun', location: '21.1619,-86.8515' },
          { name: 'Puebla', location: '19.0413,-98.2062' },
        ],
        'United Kingdom': [
          { name: 'London', location: '51.5074,-0.1278' },
          { name: 'Edinburgh', location: '55.9533,-3.1883' },
          { name: 'Manchester', location: '53.4808,-2.2426' },
          { name: 'Birmingham', location: '52.4862,-1.8904' },
          { name: 'Glasgow', location: '55.8642,-4.2518' },
        ],
        'Germany': [
          { name: 'Berlin', location: '52.5200,13.4050' },
          { name: 'Munich', location: '48.1351,11.5820' },
          { name: 'Frankfurt', location: '50.1109,8.6821' },
          { name: 'Hamburg', location: '53.5511,9.9937' },
          { name: 'Cologne', location: '50.9375,6.9603' },
        ],
        'Thailand': [
          { name: 'Bangkok', location: '13.7563,100.5018' },
          { name: 'Chiang Mai', location: '18.7883,98.9853' },
          { name: 'Phuket', location: '7.8804,98.3923' },
          { name: 'Pattaya', location: '12.9236,100.8825' },
          { name: 'Ayutthaya', location: '14.3532,100.5683' },
        ],
        'Turkey': [
          { name: 'Istanbul', location: '41.0082,28.9784' },
          { name: 'Ankara', location: '39.9334,32.8597' },
          { name: 'Izmir', location: '38.4237,27.1428' },
          { name: 'Antalya', location: '36.8841,30.7056' },
          { name: 'Bursa', location: '40.1950,29.0600' },
        ],
        'Australia': [
          { name: 'Sydney', location: '-33.8688,151.2093' },
          { name: 'Melbourne', location: '-37.8136,144.9631' },
          { name: 'Brisbane', location: '-27.4698,153.0251' },
          { name: 'Perth', location: '-31.9505,115.8605' },
          { name: 'Adelaide', location: '-34.9285,138.6007' },
        ],
        'Brazil': [
          { name: 'Rio de Janeiro', location: '-22.9068,-43.1729' },
          { name: 'Sao Paulo', location: '-23.5505,-46.6333' },
          { name: 'Brasilia', location: '-15.7942,-47.8822' },
          { name: 'Salvador', location: '-12.9777,-38.5016' },
          { name: 'Fortaleza', location: '-3.7319,-38.5267' },
        ],
        'Canada': [
          { name: 'Toronto', location: '43.6532,-79.3832' },
          { name: 'Vancouver', location: '49.2827,-123.1207' },
          { name: 'Montreal', location: '45.5017,-73.5673' },
          { name: 'Calgary', location: '51.0447,-114.0719' },
          { name: 'Ottawa', location: '45.4215,-75.6972' },
        ],
        'India': [
          { name: 'New Delhi', location: '28.6139,77.2090' },
          { name: 'Mumbai', location: '19.0760,72.8777' },
          { name: 'Bangalore', location: '12.9716,77.5946' },
          { name: 'Chennai', location: '13.0827,80.2707' },
          { name: 'Kolkata', location: '22.5726,88.3639' },
        ],
        'South Africa': [
          { name: 'Johannesburg', location: '-26.2041,28.0473' },
          { name: 'Cape Town', location: '-33.9249,18.4241' },
          { name: 'Durban', location: '-29.8587,31.0218' },
          { name: 'Pretoria', location: '-25.7479,28.2293' },
          { name: 'Port Elizabeth', location: '-33.9608,25.6022' },
        ],
        'Russia': [
          { name: 'Moscow', location: '55.7558,37.6176' },
          { name: 'Saint Petersburg', location: '59.9343,30.3351' },
          { name: 'Novosibirsk', location: '55.0084,82.9357' },
          { name: 'Yekaterinburg', location: '56.8389,60.6057' },
          { name: 'Kazan', location: '55.8304,49.0661' },
        ],
        'Argentina': [
          { name: 'Buenos Aires', location: '-34.6037,-58.3816' },
          { name: 'Cordoba', location: '-31.4201,-64.1888' },
          { name: 'Rosario', location: '-32.9468,-60.6393' },
          { name: 'Mendoza', location: '-32.8895,-68.8458' },
          { name: 'La Plata', location: '-34.9205,-57.9545' },
        ],
        'Netherlands': [
          { name: 'Amsterdam', location: '52.3676,4.9041' },
          { name: 'Rotterdam', location: '51.9244,4.4777' },
          { name: 'The Hague', location: '52.0705,4.3007' },
          { name: 'Utrecht', location: '52.0907,5.1214' },
          { name: 'Eindhoven', location: '51.4416,5.4697' },
        ],
        'Greece': [
          { name: 'Athens', location: '37.9838,23.7275' },
          { name: 'Thessaloniki', location: '40.6401,22.9444' },
          { name: 'Patras', location: '38.2466,21.7346' },
          { name: 'Heraklion', location: '35.3387,25.1442' },
          { name: 'Larissa', location: '39.6390,22.4194' },
        ],
        'Malaysia': [
          { name: 'Kuala Lumpur', location: '3.1390,101.6869' },
          { name: 'George Town', location: '5.4141,100.3288' },
          { name: 'Johor Bahru', location: '1.4927,103.7414' },
          { name: 'Kota Kinabalu', location: '5.9804,116.0735' },
          { name: 'Malacca City', location: '2.1896,102.2501' },
        ],
        'Egypt': [
          { name: 'Cairo', location: '30.0444,31.2357' },
          { name: 'Alexandria', location: '31.2001,29.9187' },
          { name: 'Giza', location: '30.0131,31.2089' },
          { name: 'Luxor', location: '25.6872,32.6396' },
          { name: 'Aswan', location: '24.0889,32.8998' },
        ],
        'Switzerland': [
          { name: 'Zurich', location: '47.3769,8.5417' },
          { name: 'Geneva', location: '46.2044,6.1432' },
          { name: 'Basel', location: '47.5596,7.5886' },
          { name: 'Bern', location: '46.8182,8.2275' },
          { name: 'Lausanne', location: '46.5197,6.6323' },
        ],
        'Indonesia': [
          { name: 'Jakarta', location: '-6.2088,106.8456' },
          { name: 'Bali (Denpasar)', location: '-8.6500,115.2167' },
          { name: 'Surabaya', location: '-7.2575,112.7521' },
          { name: 'Bandung', location: '-6.9175,107.6191' },
          { name: 'Yogyakarta', location: '-7.7956,110.3695' },
        ],
        'Portugal': [
          { name: 'Lisbon', location: '38.7223,-9.1393' },
          { name: 'Porto', location: '41.1579,-8.6291' },
          { name: 'Faro', location: '37.0194,-7.9304' },
          { name: 'Coimbra', location: '40.2033,-8.4103' },
          { name: 'Braga', location: '41.5453,-8.4265' },
        ],
        'Austria': [
          { name: 'Vienna', location: '48.2082,16.3738' },
          { name: 'Salzburg', location: '47.8095,13.0550' },
          { name: 'Innsbruck', location: '47.2692,11.4041' },
          { name: 'Graz', location: '47.0707,15.4395' },
          { name: 'Linz', location: '48.3069,14.2858' },
        ],
        'Sweden': [
          { name: 'Stockholm', location: '59.3293,18.0686' },
          { name: 'Gothenburg', location: '57.7089,11.9746' },
          { name: 'Malmö', location: '55.604981,13.003822' },
          { name: 'Uppsala', location: '59.8586,17.6389' },
          { name: 'Västerås', location: '59.6168,16.5528' },
        ],
        'Vietnam': [
          { name: 'Hanoi', location: '21.0285,105.8542' },
          { name: 'Ho Chi Minh City', location: '10.8231,106.6297' },
          { name: 'Da Nang', location: '16.0544,108.2022' },
          { name: 'Hue', location: '16.4637,107.5908' },
          { name: 'Nha Trang', location: '12.2388,109.1967' },
        ],
        'Singapore': [
          { name: 'Singapore', location: '1.3521,103.8198' },
        ],
        'New Zealand': [
          { name: 'Auckland', location: '-36.8485,174.7633' },
          { name: 'Wellington', location: '-41.2865,174.7762' },
          { name: 'Christchurch', location: '-43.5321,172.6362' },
          { name: 'Hamilton', location: '-37.7870,175.2793' },
          { name: 'Dunedin', location: '-45.8788,170.5028' },
        ],
        'Poland': [
          { name: 'Warsaw', location: '52.2297,21.0122' },
          { name: 'Krakow', location: '50.0647,19.9450' },
          { name: 'Gdansk', location: '54.3520,18.6466' },
          { name: 'Wroclaw', location: '51.1079,17.0385' },
          { name: 'Poznan', location: '52.4064,16.9252' },
        ],
        'Morocco': [
          { name: 'Casablanca', location: '33.5731,-7.5898' },
          { name: 'Marrakesh', location: '31.6295,-7.9811' },
          { name: 'Rabat', location: '34.0209,-6.8416' },
          { name: 'Fez', location: '34.0181,-5.0064' },
          { name: 'Tangier', location: '35.7595,-5.8339' },
        ],
        'Philippines': [
          { name: 'Manila', location: '14.5995,120.9842' },
          { name: 'Cebu City', location: '10.3157,123.8854' },
          { name: 'Davao City', location: '7.1907,125.4553' },
          { name: 'Baguio', location: '16.4023,120.5960' },
          { name: 'Iloilo City', location: '10.7201,122.5621' },
        ],
        'Chile': [
          { name: 'Santiago', location: '-33.4489,-70.6693' },
          { name: 'Valparaiso', location: '-33.0472,-71.6127' },
          { name: 'Concepcion', location: '-36.8201,-73.0444' },
          { name: 'La Serena', location: '-29.9045,-71.2451' },
          { name: 'Antofagasta', location: '-23.6505,-70.3975' },
        ],
        'South Korea': [
          { name: 'Seoul', location: '37.5665,126.9780' },
          { name: 'Busan', location: '35.1796,129.0756' },
          { name: 'Incheon', location: '37.4563,126.7052' },
          { name: 'Daegu', location: '35.8722,128.6025' },
          { name: 'Daejeon', location: '36.3504,127.3845' },
        ],
        'United Arab Emirates': [
          { name: 'Dubai', location: '25.276987,55.296249' },
          { name: 'Abu Dhabi', location: '24.4539,54.3773' },
          { name: 'Sharjah', location: '25.3463,55.4209' },
          { name: 'Al Ain', location: '24.2074,55.7608' },
          { name: 'Ras Al Khaimah', location: '25.8000,55.9833' },
        ],
        'Czech Republic': [
          { name: 'Prague', location: '50.0755,14.4378' },
          { name: 'Brno', location: '49.1951,16.6068' },
          { name: 'Ostrava', location: '49.8209,18.2625' },
          { name: 'Plzen', location: '49.7475,13.3771' },
          { name: 'Liberec', location: '50.7670,15.0562' },
        ],
        'Saudi Arabia': [
          { name: 'Riyadh', location: '24.7136,46.6753' },
          { name: 'Jeddah', location: '21.4858,39.1925' },
          { name: 'Mecca', location: '21.3891,39.8579' },
          { name: 'Medina', location: '24.5247,39.5692' },
          { name: 'Dammam', location: '26.3927,50.0888' },
        ],
        'Belgium': [
          { name: 'Brussels', location: '50.8503,4.3517' },
          { name: 'Antwerp', location: '51.2194,4.4025' },
          { name: 'Ghent', location: '51.0543,3.7174' },
          { name: 'Bruges', location: '51.2093,3.2247' },
          { name: 'Leuven', location: '50.8798,4.7005' },
        ],
        'Israel': [
          { name: 'Jerusalem', location: '31.7683,35.2137' },
          { name: 'Tel Aviv', location: '32.0853,34.7818' },
          { name: 'Haifa', location: '32.7940,34.9896' },
          { name: 'Eilat', location: '29.5581,34.9482' },
          { name: 'Beersheba', location: '31.2518,34.7913' },
        ],
        'Peru': [
          { name: 'Lima', location: '-12.0464,-77.0428' },
          { name: 'Cusco', location: '-13.5319,-71.9675' },
          { name: 'Arequipa', location: '-16.4090,-71.5375' },
          { name: 'Trujillo', location: '-8.1164,-79.0283' },
          { name: 'Chiclayo', location: '-6.7764,-79.8403' },
        ],
        'Norway': [
          { name: 'Oslo', location: '59.9139,10.7522' },
          { name: 'Bergen', location: '60.3913,5.3221' },
          { name: 'Trondheim', location: '63.4305,10.3951' },
          { name: 'Stavanger', location: '58.9690,5.7331' },
          { name: 'Tromsø', location: '69.6492,18.9560' },
        ],
        'Denmark': [
          { name: 'Copenhagen', location: '55.6761,12.5683' },
          { name: 'Aarhus', location: '56.1629,10.2039' },
          { name: 'Odense', location: '55.4038,10.4024' },
          { name: 'Aalborg', location: '57.0467,9.9187' },
          { name: 'Esbjerg', location: '55.4765,8.4594' },
        ],
        'Hungary': [
          { name: 'Budapest', location: '47.4979,19.0402' },
          { name: 'Debrecen', location: '47.5316,21.6273' },
          { name: 'Szeged', location: '46.2530,20.1414' },
          { name: 'Miskolc', location: '48.1039,20.7944' },
          { name: 'Pécs', location: '46.0727,18.2323' },
        ],
        'Ireland': [
          { name: 'Dublin', location: '53.3498,-6.2603' },
          { name: 'Cork', location: '51.8985,-8.4756' },
          { name: 'Galway', location: '53.2707,-9.0568' },
          { name: 'Limerick', location: '52.6638,-8.6267' },
          { name: 'Waterford', location: '52.2593,-7.1100' },
        ],
        'Finland': [
          { name: 'Helsinki', location: '60.1695,24.9354' },
          { name: 'Espoo', location: '60.2055,24.6559' },
          { name: 'Tampere', location: '61.4978,23.7610' },
          { name: 'Vantaa', location: '60.2934,25.0403' },
          { name: 'Oulu', location: '65.0121,25.4682' },
        ],
        'Colombia': [
          { name: 'Bogotá', location: '4.7110,-74.0721' },
          { name: 'Medellín', location: '6.2442,-75.5812' },
          { name: 'Cali', location: '3.4516,-76.5319' },
          { name: 'Cartagena', location: '10.3910,-75.4794' },
          { name: 'Barranquilla', location: '10.9685,-74.7813' },
        ],
        'Ukraine': [
          { name: 'Kyiv', location: '50.4501,30.5234' },
          { name: 'Lviv', location: '49.8397,24.0297' },
          { name: 'Odessa', location: '46.4825,30.7233' },
          { name: 'Kharkiv', location: '49.9935,36.2304' },
          { name: 'Dnipro', location: '48.4647,35.0462' },
        ],
        // Add more countries and their cities as needed
      };
      return cities[country] || [];
    },
    goBack() {
      this.$router.go(-1);
    },
    showSavedPopup() {
      this.showPopup = true; // Show the popup
      setTimeout(() => {
        this.showPopup = false; // Automatically hide after 3 seconds
      }, 3000);
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
            name: attraction.name || 'Unknown',
            vicinity: attraction.vicinity || 'Unknown vicinity',
            image: attraction.image || '/default-image.jpg',
            coordinates: attraction.coordinates,
            rating: attraction.rating || 0,
            user_ratings_total: attraction.user_ratings_total || 0,
            open_now: attraction.open_now || false,
          };

          try {
            const userRef = doc(db, "users", this.userId);
            const userDoc = await getDoc(userRef);

            if (userDoc.exists()) {
              const existingSavedPlaces = userDoc.data().savedPlaces || [];

              // Check if the place already exists
              const placeExists = existingSavedPlaces.some(
                (savedPlace) => savedPlace.place_id === placeData.place_id
              );

              if (placeExists) {
                console.log("Place already saved:", placeData.name);
                return; // Exit if already saved
              }
            }

            // If not already saved, save the new place
            await setDoc(
              userRef,
              {
                savedPlaces: arrayUnion(placeData),
              },
              { merge: true }
            );
            console.log("Place added to saved places:", placeData.name);
            this.showSavedPopup();

            // Update the global savedPlacesState
            if (this.savedPlacesState && Array.isArray(this.savedPlacesState.savedPlaces)) {
              this.savedPlacesState.savedPlaces.push(placeData);
            }
          } catch (error) {
            console.error("Error saving place to Firebase:", error);
            this.errorMessage = 'Failed to save the place. Please try again.';
          }
        } else {
          console.error("Attraction not found for saving.");
          this.errorMessage = 'Attraction data is missing. Unable to save.';
        }
      } else {
        console.error("User is not authenticated");
        this.errorMessage = 'You must be logged in to save places.';
      }
    },
    async generateItinerary() {
      // Implement your itinerary generation logic here
      console.log("Generate Itinerary button clicked");
      // This could involve creating a new itinerary document in Firestore
    }
  },
  mounted() {
    // Listen for authentication state changes
    auth.onAuthStateChanged((user) => {
      if (user) {
        this.userId = user.uid;
        // Load saved places for the authenticated user
        if (this.savedPlacesState && typeof this.savedPlacesState.loadSavedPlaces === 'function') {
          this.savedPlacesState.loadSavedPlaces(user.uid);
        }
      } else {
        console.error("User is not authenticated");
        this.userId = null;
        // Clear the global savedPlacesState
        if (this.savedPlacesState && typeof this.savedPlacesState.clearSavedPlaces === 'function') {
          this.savedPlacesState.clearSavedPlaces();
        }
      }
    });
  }
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap");

.destination-details {
  text-align: center;
}

.header-row {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px 5%;
  position: relative;
}

.back-button {
  position: absolute;
  left: 5%;
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
  font-size: 2rem; /* Adjusted font size */
  color: black;
  font-weight: bolder;
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

.attractions-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.attraction-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin: 20px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 10px;
  width: 220px;
  height: 500px; /* Increased height to accommodate additional data */
  text-align: center;
  background-color: #fff;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.attraction-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}

.attraction-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 5px;
  margin-bottom: 10px;
}

.attraction-name {
  font-size: 1rem;
  margin: 10px 0;
  color: black;
  white-space: normal;
  overflow: visible;
}

.attraction-vicinity {
  font-size: 0.8rem;
  color: gray;
  white-space: normal;
  overflow: visible;
}

.attraction-rating {
  font-size: 0.9rem;
  color: #f39c12; /* Gold color for ratings */
}

.attraction-hours {
  font-size: 0.9rem;
  color: #27ae60; /* Green for open, red for closed */
}

.save-button {
  margin-top: auto;
  background-color: black;
  color: white;
  padding: 8px;
  font-size: 0.8rem;
  font-weight: bold;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.save-button:hover {
  background-color: #333;
  color: white;
}

@media (max-width: 768px) {
  .attraction-card {
    width: 90%;
    height: auto;
  }
}

.popup {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: green;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  transition: opacity 0.3s ease;
  opacity: 1;
}
</style>
