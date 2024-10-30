<template>
  <div class="destination-details">
    <!-- Toast Notification Component -->
    <ToastNotification
      :show="showToast"
      :title="toastTitle"
      :message="toastMessage"
      :type="toastType"
      @update:show="showToast = $event"
    />

    <div class="header-row">
      <button @click="goBack" class="btn back-button">Back to Destinations</button>
      <h1 class="page-title">Top Tourist Attractions in {{ country }}</h1>
    </div>

    <div v-if="loading" class="loading">Loading...</div>

    <div v-if="!loading" class="attractions-list">
      <div v-for="attraction in attractions" :key="attraction.place_id" class="attraction-card">
        <img :src="attraction.image" alt="attraction-image" class="attraction-image" />
        <h2 class="attraction-name">{{ attraction.name }}</h2>
        <p class="attraction-vicinity">{{ attraction.vicinity }}</p>

        <!-- Save/Remove Button -->
        <button
          class="btn save-button"
          @click="toggleSavePlace(attraction)"
        >
          {{ isPlaceSaved(attraction.place_id) ? 'Remove from Saved Places' : 'Save Place' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import ToastNotification from "@/components/ToastNotification.vue"; // Adjust the path as needed
import { getFirestore, doc, getDoc, runTransaction, arrayUnion } from "firebase/firestore";
import { getAuth } from "firebase/auth";
import axios from "axios";

export default {
  name: "DestinationDetails",
  components: {
    ToastNotification,
  },
  data() {
    return {
      attractions: [],
      loading: true,
      country: this.$route.params.country,
      apiKey: 'AIzaSyAlRNUntEwMM5zLz3LaPQiJF68cw9uL4rE', // Replace with your actual API key
      cityName: this.$route.params.city || 'Unknown City',
      userId: null,
      savedPlaces: [],
      showToast: false,
      toastTitle: '',
      toastMessage: '',
      toastType: '', // 'add' or 'remove'
    };
  },
  created() {
    this.fetchAttractions();
  },
  methods: {
    async toggleSavePlace(attraction) {
      if (this.isPlaceSaved(attraction.place_id)) {
        await this.removePlaceFromFirebase(attraction);
      } else {
        await this.savePlaceToFirebase(attraction);
      }
    },

    async savePlaceToFirebase(attraction) {
      const auth = getAuth();
      const user = auth.currentUser;

      if (user) {
        this.userId = user.uid;
        const db = getFirestore();
        const userRef = doc(db, "users", this.userId);

        const placeData = {
          place_id: attraction.place_id || null,
          name: attraction.name || 'Unknown',
          vicinity: attraction.vicinity || 'Unknown vicinity',
          image: attraction.image || '/default-image.jpg',
          coordinates: attraction.coordinates || null,
        };

        try {
          await runTransaction(db, async (transaction) => {
            const userDoc = await transaction.get(userRef);
            if (!userDoc.exists()) {
              transaction.set(userRef, { savedPlaces: [placeData] });
            } else {
              transaction.update(userRef, {
                savedPlaces: arrayUnion(placeData),
              });
            }
          });

          // Update local savedPlaces
          this.savedPlaces.push(placeData);

          // Trigger Toast Notification
          this.triggerToast('Added to Saved Places!', 'add');
        } catch (error) {
          console.error("Error saving place to Firebase:", error);
        }
      } else {
        console.error("User is not authenticated");
      }
    },

    async removePlaceFromFirebase(attraction) {
      const auth = getAuth();
      const user = auth.currentUser;

      if (user) {
        this.userId = user.uid;
        const db = getFirestore();
        const userRef = doc(db, "users", this.userId);

        const placeData = {
          place_id: attraction.place_id || null,
          name: attraction.name || 'Unknown',
          vicinity: attraction.vicinity || 'Unknown vicinity',
          image: attraction.image || '/default-image.jpg',
          coordinates: attraction.coordinates || null,
        };

        try {
          await runTransaction(db, async (transaction) => {
            const userDoc = await transaction.get(userRef);
            if (userDoc.exists()) {
              const existingSavedPlaces = userDoc.data().savedPlaces || [];

              const updatedSavedPlaces = existingSavedPlaces.filter(
                (savedPlace) => savedPlace.place_id !== placeData.place_id
              );

              transaction.update(userRef, {
                savedPlaces: updatedSavedPlaces,
              });
            }
          });

          // Update local savedPlaces
          this.savedPlaces = this.savedPlaces.filter(
            (savedPlace) => savedPlace.place_id !== placeData.place_id
          );

          // Trigger Toast Notification
          this.triggerToast('Removed from Saved Places!', 'remove');
        } catch (error) {
          console.error("Error removing place from Firebase:", error);
        }
      } else {
        console.error("User is not authenticated");
      }
    },

    isPlaceSaved(placeId) {
      return this.savedPlaces.some((place) => place.place_id === placeId);
    },

    triggerToast(message, type) {
      this.toastMessage = message;
      this.toastType = type;
      this.showToast = true;
    },

    async fetchAttractions() {
      const location = this.getCountryCoordinates(this.country);
      if (!location) {
        console.error(`No coordinates found for ${this.country}`);
        this.loading = false;
        return;
      }

      const radius = 50000;
      const type = "tourist_attraction";
      const url = `/api/maps/api/place/nearbysearch/json?location=${location}&radius=${radius}&type=${type}&key=${this.apiKey}`;

      try {
        const response = await axios.get(url);
        console.log("Fetched attractions:", response.data.results);
        this.attractions = response.data.results.map((place) => ({
          name: place.name,
          place_id: place.place_id,
          vicinity: place.vicinity,
          image: place.photos
            ? `https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${place.photos[0].photo_reference}&key=${this.apiKey}`
            : "/default-image.jpg",
          coordinates: {
            latitude: place.geometry.location.lat,
            longitude: place.geometry.location.lng,
          },
        }));
        this.loading = false;
      } catch (error) {
        console.error("Error fetching attractions:", error);
        this.loading = false;
      }
    },

    getCountryCoordinates(country) {
      const coordinates = {
        'France': '48.8566,2.3522',
        'Italy': '41.9028,12.4964',
        'Japan': '35.6895,139.6917',
        'United States': '37.7749,-122.4194',
        'Spain': '40.4168,-3.7038',
        'China': '39.9042,116.4074',
        'Mexico': '19.4326,-99.1332',
        'United Kingdom': '51.5074,-0.1278',
        'Germany': '52.5200,13.4050',
        'Thailand': '13.7563,100.5018',
        'Turkey': '41.0082,28.9784',
        'Australia': '-33.8688,151.2093',
        'Brazil': '-23.5505,-46.6333',
        'Canada': '45.4215,-75.6972',
        'India': '28.6139,77.2090',
        'South Africa': '-25.7461,28.1881',
        'Russia': '55.7558,37.6176',
        'Argentina': '-34.6037,-58.3816',
        'Netherlands': '52.3676,4.9041',
        'Greece': '37.9838,23.7275',
        'Malaysia': '3.1390,101.6869',
        'Egypt': '30.0444,31.2357',
        'Switzerland': '46.9481,7.4474',
        'Indonesia': '-6.2088,106.8456',
        'Portugal': '38.7223,-9.1393',
        'Austria': '48.2082,16.3738',
        'Sweden': '59.3293,18.0686',
        'Vietnam': '21.0285,105.8542',
        'Singapore': '1.3521,103.8198',
        'New Zealand': '-36.8485,174.7633',
        'Poland': '52.2297,21.0122',
        'Morocco': '31.6295,-7.9811',
        'Philippines': '14.5995,120.9842',
        'Chile': '-33.4489,-70.6693',
        'South Korea': '37.5665,126.9780',
        'United Arab Emirates': '25.2048,55.2708',
        'Czech Republic': '50.0755,14.4378',
        'Saudi Arabia': '24.7136,46.6753',
        'Belgium': '50.8503,4.3517',
        'Israel': '31.7683,35.2137',
        'Peru': '-12.0464,-77.0428',
        'Norway': '59.9139,10.7522',
        'Denmark': '55.6761,12.5683',
        'Hungary': '47.4979,19.0402',
        'Ireland': '53.3498,-6.2603',
        'Finland': '60.1695,24.9354',
        'Colombia': '4.7110,-74.0721',
        'Ukraine': '50.4501,30.5234',
        'Ghana': '5.6037,-0.1870',
        'Kenya': '-1.2921,36.8219',
        'Tanzania': '-6.7924,39.2083',
        'Uganda': '0.3476,32.5825',
        'Nigeria': '6.5244,3.3792',
        'Ethiopia': '9.1450,40.4897',
        'Zambia': '-15.3875,28.3228',
        'Zimbabwe': '-17.8252,31.0335',
        'Botswana': '-24.6282,25.9231',
        'Namibia': '-22.5609,17.0658',
        'Angola': '-8.8390,13.2894',
        'Mozambique': '-25.9692,32.5732',
        'Algeria': '36.7538,3.0588',
        'Tunisia': '36.8065,10.1815',
        'Libya': '32.8872,13.1913',
        'Sudan': '15.5007,32.5599',
        'Iceland': '64.1466,-21.9426',
        'Cuba': '23.1136,-82.3666',
        'Jamaica': '18.1096,-77.2975',
        'Bahamas': '25.0443,-77.3504',
        'Dominican Republic': '18.4861,-69.9312',
        'Puerto Rico': '18.2208,-66.5901',
        'Panama': '8.9824,-79.5199',
        'Costa Rica': '9.9281,-84.0907',
        'Honduras': '14.0723,-87.1921',
        'Guatemala': '14.6349,-90.5069',
        'El Salvador': '13.6929,-89.2182',
        'Nicaragua': '12.1150,-86.2362',
        'Belize': '17.5046,-88.1962',
        'Luxembourg': '49.6116,6.1319',
        'Monaco': '43.7384,7.4246',
        'Liechtenstein': '47.1411,9.5209',
        'Malta': '35.9375,14.3754',
        'Cyprus': '35.1856,33.3823',
        'Latvia': '56.9496,24.1052',
        'Lithuania': '54.6872,25.2797',
        'Estonia': '59.4370,24.7536',
        'Slovakia': '48.1486,17.1077',
        'Slovenia': '46.0569,14.5058',
        'Croatia': '45.8150,15.9819',
        'Romania': '44.4268,26.1025',
        'Bulgaria': '42.6977,23.3219',
        'Serbia': '44.7866,20.4489',
        'Macedonia': '41.9981,21.4254',
        'Albania': '41.3275,19.8187',
        'Montenegro': '42.4304,19.2594',
        'Bosnia and Herzegovina': '43.8563,18.4131',
        'Belarus': '53.9045,27.5615',
        'Moldova': '47.0105,28.8638',
        'Georgia': '41.7151,44.8271',
        'Armenia': '40.1792,44.4991',
        'Azerbaijan': '40.4093,49.8671',
        'Kazakhstan': '51.1605,71.4704',
        'Uzbekistan': '41.2995,69.2401',
        'Kyrgyzstan': '42.8746,74.5698',
        'Tajikistan': '38.5598,68.7870',
        'Turkmenistan': '37.9601,58.3261',
        'Afghanistan': '34.5553,69.2075',
        'Pakistan': '33.6844,73.0479',
        'Bangladesh': '23.8103,90.4125',
        'Sri Lanka': '6.9271,79.8612',
        'Nepal': '27.7172,85.3240',
        'Bhutan': '27.4728,89.6393',
        'Myanmar': '16.8409,96.1735',
        'Cambodia': '11.5564,104.9282',
        'Laos': '17.9757,102.6331',
        'Brunei': '4.9031,114.9398',
        'Papua New Guinea': '-9.4438,147.1803',
        'Fiji': '-18.1248,178.4501',
        'Samoa': '-13.7590,-172.1046',
        'Vanuatu': '-17.7333,168.3273',
        'Solomon Islands': '-9.6457,160.1562',
        'Micronesia': '6.9248,158.1610',
        'Palau': '7.5149,134.5825',
        'Marshall Islands': '7.1164,171.1850',
        'Kiribati': '1.4518,173.0374',
        'Maldives': '4.1755,73.5093',
        'Seychelles': '-4.6796,55.4920',
        'Mauritius': '-20.1609,57.5012',
        'Madagascar': '-18.8792,47.5079',
        'Reunion': '-20.8821,55.4507',
        'French Polynesia': '-17.6797,-149.4068',
        'New Caledonia': '-22.2558,166.4505',
        'Guam': '13.4443,144.7937',
        'Northern Mariana Islands': '15.0979,145.6739',
        'American Samoa': '-14.3064,-170.6950',
        'Guadeloupe': '16.2650,-61.5500',
        'Martinique': '14.6415,-61.0242',
        'Aruba': '12.5211,-69.9683',
        'Curacao': '12.1696,-68.9900',
        'Bermuda': '32.3078,-64.7505',
        'Cayman Islands': '19.3133,-81.2546',
        'Turks and Caicos Islands': '21.6940,-71.7979',
        'British Virgin Islands': '18.4207,-64.6399',
        'Anguilla': '18.2206,-63.0686',
        'Montserrat': '16.7425,-62.1874',
        'Antigua and Barbuda': '17.0608,-61.7964',
        'Barbados': '13.1939,-59.5432',
        'Grenada': '12.1165,-61.6790',
        'Dominica': '15.3092,-61.3790',
        'Saint Lucia': '13.9094,-60.9789',
        'Saint Vincent and the Grenadines': '13.2528,-61.1971',
        'Trinidad and Tobago': '10.6918,-61.2225',
        'Guyana': '6.8013,-58.1551',
        'Suriname': '5.8520,-55.2038',
        'French Guiana': '4.9224,-52.3260',
        'Venezuela': '10.4806,-66.9036',
        'Ecuador': '-0.1807,-78.4678',
        'Bolivia': '-16.4897,-68.1193',
        'Paraguay': '-25.2637,-57.5759',
        'Uruguay': '-34.9011,-56.1645',
        'Greenland': '64.1814,-51.6941',
        'Iraq': '33.3152,44.3661',
        'Iran': '35.6892,51.3890',
        'Syria': '33.5138,36.2765',
        'Lebanon': '33.8938,35.5018',
        'Jordan': '31.9539,35.9106',
        'Oman': '23.5880,58.3829',
        'Qatar': '25.2854,51.5310',
        'Kuwait': '29.3759,47.9774',
        'Bahrain': '26.2285,50.5861',
        'Yemen': '15.3694,44.1910',
        'North Korea': '39.0392,125.7625',
        'Mongolia': '47.8864,106.9057',
      };
      return coordinates[country] || null;
    },

    goBack() {
      this.$router.go(-1);
    },
  },
  mounted() {
    const auth = getAuth();
    auth.onAuthStateChanged(async (user) => {
      if (user) {
        this.userId = user.uid;
        const db = getFirestore();
        const userRef = doc(db, "users", this.userId);

        try {
          const userDoc = await getDoc(userRef);
          if (userDoc.exists()) {
            this.savedPlaces = userDoc.data().savedPlaces || [];
          }
        } catch (error) {
          console.error("Error fetching saved places:", error);
        }
      } else {
        console.error("User is not authenticated");
      }
    });
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap");

.destination-details {
  text-align: center;
  font-family: "Roboto", sans-serif;
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
  font-size: rem;
  color: black;
  font-family: 'Cormorant Garamond', serif;
  font-weight: bolder;
}

.loading {
  font-size: 1.5rem;
  margin: 50px;
  color: black;
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
  height: 400px;
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

h2.attraction-name {
  font-size: 1rem;
  margin: 10px 0;
  color: black;
  white-space: normal;
  overflow: visible;
}

p.attraction-vicinity {
  font-size: 0.8rem;
  color: gray;
  white-space: normal;
  overflow: visible;
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
</style>
