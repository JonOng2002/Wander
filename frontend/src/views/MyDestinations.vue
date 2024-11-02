<template>
  <header id="headercard">
    <div class="header_image"></div>
    <div class="header_container">
      <div class="content">
        <h1>Unleash the Magic of Travel.</h1>
        <h4>Adventure Awaits—Choose Your Dream Destination Now.</h4>
      </div>
    </div>
  </header>

  <div class="secondary_header">
    <div class="secondary_content">
      <h2>Top Destinations for your next holiday</h2>
      <h5>Here's where your fellow wanderers are headed:</h5>
    </div>

    <!-- Custom Dropdowns for sorting and filtering -->
    <div class="filter-container">
      <!-- Sort by Dropdown -->
      <div class="dropdown" @click="toggleDropdown('sort')">
        <button class="dropdown-btn">
          Filter by: {{ sortLabel }}
          <span class="arrow-down">&#9662;</span>
        </button>
        <ul :style="{ display: showDropdowns.sort ? 'block' : 'none' }" class="dropdown-menu">
          <li @click.stop="selectSort('default')">Top Destinations</li>
          <li @click.stop="selectSort('alphabetical')">Alphabetical Order</li>

        </ul>
      </div>

      <!-- Filter by Continent Dropdown -->
      <div class="dropdown" @click="toggleDropdown('filter')">
        <button class="dropdown-btn">
          Filter by Continent: {{ filterLabel }}
          <span class="arrow-down">&#9662;</span>
        </button>
        <ul :style="{ display: showDropdowns.filter ? 'block' : 'none' }" class="dropdown-menu">
          <li @click.stop="selectContinent('')">All Continents</li>
          <li @click.stop="selectContinent('Europe')">Europe</li>
          <li @click.stop="selectContinent('Asia')">Asia</li>
          <li @click.stop="selectContinent('North America')">North America</li>
          <li @click.stop="selectContinent('South America')">South America</li>
          <li @click.stop="selectContinent('Oceania')">Oceania</li>
          <li @click.stop="selectContinent('Africa')">Africa</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="container">
    <div class="card_container">
      <article v-for="country in filteredCountries" :key="country.code" class="card_article">
        <div class="text_overlay">{{ country.name }}</div>

        <img :src="country.image" alt="country-image" class="card_img" loading="lazy" />

        <div class="card_data">
          <span class="card_description">
            {{ country.name }}, {{ getRegion(country.name) }}
          </span>
          <h2 class="card_title">{{ country.place }}</h2>
          <p class="country_description">{{ country.description }}</p>
          <a href="#" class="card_button" @click="goToDestinationDetails(country.name)">Explore More</a>
        </div>
      </article>
    </div>
  </div>
</template>


<script>
export default {
  name: "MyDestinations",
  data() {
    return {
      countries: [
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
      ],
      sortOrder: 'default', // Track sorting order
      continentFilter: '',  // Track continent filter
      showDropdowns: { sort: false, filter: false },
      sortLabel: 'Top Destinations',
      filterLabel: 'All Continents',
    };
  },

  created() {
    // Store the original order of countries when the component is created
    this.originalCountries = [...this.countries];
  },

  computed: {
    // This computed property handles filtering and sorting
    filteredCountries() {
      let filteredList = this.countries;

      // Apply continent filter
      if (this.continentFilter) {
        filteredList = filteredList.filter(country =>
          this.getRegion(country.name) === this.continentFilter
        );
      }

      // Apply sorting
      if (this.sortOrder === 'alphabetical') {
        filteredList = filteredList.sort((a, b) => a.name.localeCompare(b.name));
      }

      return filteredList;
    },
  },


  methods: {
    getRegion(country) {
      const regions = {
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
      return regions[country] || "Unknown";
    },

    goToDestinationDetails(countryName) {
      this.$router.push({
        name: "DestinationDetails",
        params: { country: countryName },
      });
    },

    toggleDropdown(type) {
      // Toggle the dropdown visibility
      Object.keys(this.showDropdowns).forEach(key => {
        this.showDropdowns[key] = (key === type) ? !this.showDropdowns[key] : false;
      });
    },

    selectSort(order) {
      this.sortOrder = order;
      this.sortLabel = order === 'alphabetical' ? 'Alphabetical Order' : 'Top Destinations';

      if (order === 'default') {
        // Reset the countries list to the original order
        this.countries = [...this.originalCountries];
      } else if (order === 'alphabetical') {
        // Sort the countries list alphabetically
        this.countries = [...this.countries].sort((a, b) => a.name.localeCompare(b.name));
      }

      this.showDropdowns.sort = false;
    },

    selectContinent(continent) {
      this.continentFilter = continent;
      this.filterLabel = continent === '' ? 'All Continents' : continent;
      this.showDropdowns.filter = false;
    },
  },

};
</script>

<style scoped>
h1 {
  text-align: center;
}

/* Remove default margin and padding */
body,
#headercard {
  margin: 0;
  padding: 0;
}

html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
  /* Make sure the body takes up the full viewport */
  background-color: #2a5ead;
}

/*====== HEADER ======*/


header {
  position: relative;
  overflow: hidden;
  min-height: 60vh;
  /* Minimum height to prevent cutoffs */
  display: flex;
  align-items: center;
  /* Center contents vertically */
  justify-content: center;
}

.header_image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("@/assets/background_header.jpeg");
  background-size: cover;
  /* Prevents cropping */
  background-position: center;
  background-repeat: no-repeat;
  z-index: -1;
}

.header_container {
  text-align: center;
  color: white;
  max-width: 90%;
  margin: 0 auto;
  z-index: 1;
}

header .content h1 {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

header content h4 {
  color: hsl(0, 0%, 70%);
  font-size: 1.25rem;
  font-weight: 500;
}

/*====== SECONDARY HEADER ======*/

.secondary_header {
  position: relative;
  left: 50px;
  top: 60px;
  padding-bottom: 1rem;
}

.secondary_content h5 {
  color: rgb(166, 163, 163);
  margin-bottom: 1rem;
}

/* Dropdown button styling */
.dropdown-btn {
  background-color: #222;
  color: #fff;
  border: none;
  text-align: left;
  width: 320px;
  /* Consistent width with the dropdown */
  padding: 1rem;
  cursor: pointer;
  display: flex;
  /* Use flexbox for alignment */
  justify-content: space-between;
  /* Align text and arrow */
  align-items: center;
  transition: background-color 0.3s;
  position: relative;
  border-radius: 4px;
  /* Rounded edges for buttons */
}

.dropdown-btn:hover {
  background-color: #555;
}

/* Add arrow icon to indicate dropdown */
.arrow-down {
  font-size: 0.8rem;
  /* Adjust the size of the arrow */
  color: #fff;
  margin-left: 10px;
}

/* Dropdown menu styling */
.dropdown {
  position: relative;
  display: inline-block;
  margin-right: 1rem;
}

.dropdown-menu {
  position: absolute;
  background-color: #222;
  list-style: none;
  padding: 0;
  margin: 0;
  top: 100%;
  left: 0;
  /* Align the dropdown to the left of the parent button */
  width: 320px;
  /* Same width as the parent button */
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s ease-out, visibility 0.1s linear;
}

.dropdown-menu li {
  padding: 10px;
  color: white;
  cursor: pointer;
  border-bottom: 1px solid #ccc;
  transition: background-color 0.3s;
}


.dropdown-menu li:hover {
  background-color: #333;
}

/* Show the dropdown menu on hover */
.dropdown:hover .dropdown-menu {
  opacity: 1;
  visibility: visible;
}


/*====== CARD ======*/

.container {
  display: grid;
  place-items: center;
  padding-block: 5rem;
}

.card_container {
  display: grid;
  row-gap: 3.5rem;
}

.card_article {
  position: relative;
  overflow: hidden;

  --elevation: 16;
  /* Set the elevation to 8 */
  --epx: calc(var(--elevation) * 1px);

  /* These 2 shadows serve as a border for 0-1 elevation */
  --shadow1: 0 0 1px rgba(0, 0, 0, .1);
  --shadow2: 0 1px 2px rgba(0, 0, 0, .08);

  /* Calculate the dynamic shadow based on the elevation */
  --offset-y: calc(var(--epx) + 1px);
  --blur: calc(var(--epx) * 2);
  --spread: calc(var(--epx) * 0.3);

  /* Final shadow for elevation effect */
  --shadow3:
    0 var(--offset-y) var(--blur) var(--spread) rgba(0, 0, 0, 0.2);

  /* Apply the shadows */
  box-shadow:
    var(--shadow1),
    var(--shadow2),
    var(--shadow3);

  border-radius: 1.5rem;
  transition: box-shadow 0.3s ease;
  /* Optional: smooth transitions for dynamic shadow changes */
}

.card_img {
  width: 328px;
  height: 400px;
  border-radius: 1.5rem;
}

.card_img {
  width: 328px;
  height: 400px;
  border-radius: 1.5rem;
}


/* Text overlay styling */
.text_overlay {
  position: absolute;
  top: 10px;
  left: 10px;
  color: white;
  background-color: rgba(0, 0, 0, 0.2);
  font-weight: bold;
  padding: 5px 10px;
  border-radius: 1rem;
  font-size: 1.2rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  z-index: 10;
}

.card_data {
  width: 280px;
  background-color: aliceblue;
  padding: 1.5rem 2rem;
  box-shadow: 0 8px 24px hsla(0, 0%, 0%, 0.15);
  border-radius: 1rem;
  position: absolute;
  bottom: -9rem;
  left: 0;
  right: 0;
  margin-inline: auto;
  opacity: 0;
  transition: opacity 1s 1s;
}

.card_description {
  display: block;
  font-size: 0.813rem;
  margin-bottom: 0.25rem;
}

.card_title {
  font-size: medium;
  font-weight: 500;
  color: black;
  margin-bottom: 0.75rem;
}

.card_button {
  background-color: black;
  color: white;
  border: none;
  font-size: small;
  font-weight: 500;
  text-decoration: none;
  padding: 10px 20px;
  border-radius: 5px;
  display: inline-block;
  text-align: center;
  cursor: pointer;
}

.country_description {
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.5rem;
}

.card_button:hover {
  text-decoration: underline;
  background-color: #333;
}

/* Hover animations */
.card_article:hover .card_data {
  animation: show-data 1s forwards;
  opacity: 1;
  transition: opacity 0.3s;
}

.card_article:hover {
  animation: remove-overflow 2s forwards;
}

.card_article:not(:hover) {
  animation: show-overflow 2s forwards;
}

.card_article:not(:hover) .card_data {
  animation: remove-data 1s forwards;
}

@keyframes show-data {
  50% {
    transform: translateY(-10rem);
  }

  100% {
    transform: translateY(-7rem);
  }
}

@keyframes remove-overflow {
  to {
    overflow: initial;
  }
}

@keyframes remove-data {
  0% {
    transform: translateY(-7rem);
  }

  50% {
    transform: translateY(-10rem);
  }

  100% {
    transform: translateY(7rem);
  }
}

@keyframes show-overflow {
  0% {
    overflow: initial;
    pointer-events: none;
  }

  50% {
    overflow: hidden;
  }
}

/* <========================== breakpoints =========================> */

@media screen and (max-width: 576px) {
  .container {
    margin-inline: 1rem;
  }

  .card_data {
    width: 250px;
    padding: 1rem;
  }

  header {
    height: 40vh;
    /* Reduced height for small screens */
  }

  header .content h1 {
    font-size: 1.5rem;
  }

  header .content h4 {
    font-size: 0.8rem;
  }

  .header_container {
    padding: 5px;
  }

  .secondary_header {
    text-align: left;
    padding-left: 1rem;
    /* Add padding to give some spacing from the edge */
  }

  .secondary_content h2 {
    font-size: 1.2rem;
    /* Adjust to a smaller size */
    margin-bottom: 0.5rem;
  }

  .secondary_content h5 {
    font-size: 1rem;
    /* Smaller size for supporting text */
    color: rgb(166, 163, 163);
  }

  /* Arrange filter buttons side-by-side */
  .filter-container {
    display: flex;
    flex-direction: column;
    align-items: left;
  }

  .dropdown-btn {
    width: 60%;
    /* Full width on small screens */
    margin-bottom: 0.5rem;
  }

  .dropdown-btn {
    width: 60%;
    padding: 0.8rem;
  }
}

@media (max-width: 767.99px) {

  .filter-container {
    display: flex;
    flex-direction: column;
    /* Adjust the gap value as needed */
  }

  .dropdown {
    margin-bottom: 10px;
    /* Optional if more space is needed */
  }

  header .content h1 {
    font-size: 2rem;
  }

  header .content h4 {
    font-size: 1rem;
  }

  .header_container {
    padding: 15px;
  }
}


@media screen and (min-width: 768px) {
  .card_container {
    grid-template-columns: repeat(2, 1fr);
    column-gap: 1.5rem;
  }

  header {
    height: 50vh;
    /* Slightly reduced height for medium screens */
  }

  header .content h1 {
    font-size: 3rem;
  }

  header .content h4 {
    font-size: 1.2rem;
  }

  .header_container {
    padding: 15px;
  }
}


@media screen and (min-width: 1024px) {
  .container {
    height: 100vh;
  }

  .card_container {
    grid-template-columns: repeat(3, 1fr);
  }

  .card_img {
    width: 348px;
  }

  .card_data {
    width: 316px;
    padding-inline: 2.5rem;
  }

  header {
    height: 60vh;
    /* Maintain default height for large screens */
  }

  header .content h1 {
    font-size: 4rem;
  }

  header .content h4 {
    font-size: 1.2rem;
  }

  .header_container {
    padding: 20px;
  }
}
</style>