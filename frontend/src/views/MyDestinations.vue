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
  </div>

  <div class="container">
    <div class="card_container">
      <article
        v-for="country in countries"
        :key="country.code"
        class="card_article"
        @click="goToDestinationDetails(country.name)"
      >
        <div class="text_overlay">{{ country.name }}</div>

        <img :src="country.image" alt="country-image" class="card_img" />

        <div class="card_data">
          <span class="card_description"
            >{{ country.name }}, {{ getRegion(country.name) }}</span
          >
          <h2 class="card_title">{{ country.place }}</h2>
          <p class="country_description">{{ country.description }}</p>
          <a href="#" class="card_button">Explore More</a>
        </div>
      </article>
    </div>
  </div>
</template>

<script>
export default {
  name: "WorldMap",
  data() {
    return {
      countries: [
        {
          name: "France",
          place: "Paris",
          code: "FR",
          image: require('@/assets/countries/france.jpeg'),
          description:
            "France is known for its rich culture, art, and history, including landmarks like the Eiffel Tower.",
        },
        {
          name: "Italy",
          code: "IT",
          place: "Rome",
          image: require('@/assets/countries/italy.jpeg'),
          description:
            "Rome is the cradle of Western civilization, home to iconic sites like the Colosseum and the Vatican.",
        },
        {
          name: "Japan",
          code: "JP",
          place: "Kyoto",
          image:require('@/assets/countries/japan.jpg'),
          description:
            "Kyoto is the heart of Japan's traditional culture, renowned for its temples, gardens, and geisha districts.",
        },
        {
          name: "United States",
          code: "US",
          place: "New York",
          image: require('@/assets/countries/united_states.jpg'),
          description:
            "The United States boasts a diverse landscape, from the skyscrapers of New York to the Grand Canyon.",
        },
        {
          name: "Spain",
          code: "ES",
          place: "Barcelona",
          image: require('@/assets/countries/spain.jpg'),
          description:
            "Spain is famed for its passionate flamenco music, stunning beaches, and delicious tapas.",
        },
        {
          name: "China",
          code: "CN",
          place: "Beijing",
          image: require('@/assets/countries/china.jpg'),
          description:
            "China is a land of ancient wonders, from the Great Wall to bustling cities like Beijing and Shanghai.",
        },
        {
          name: "Mexico",
          code: "MX",
          place: "Yuacatan",
          image: require('@/assets/countries/mexico.jpg'),
          description:
            "Mexico offers vibrant culture, ancient ruins like Chichen Itza, and beautiful beaches along its coastlines.",
        },
        {
          name: "United Kingdom",
          code: "GB",
          place: "London",
          image: require('@/assets/countries/united_kingdom.jpg'),
          description:
            "The United Kingdom is rich in history, from the Tower of London to the Highlands of Scotland.",
        },
        {
          name: "Germany",
          code: "DE",
          place: "Berlin",
          image: require('@/assets/countries/germany.jpg'),
          description:
            "Germany is known for its medieval castles, scenic forests, and the vibrant city of Berlin.",
        },
        {
          name: "Thailand",
          code: "TH",
          image: require('@/assets/countries/thailand.jpg'),
          description:
            "Thailand is a tropical paradise, renowned for its temples, beaches, and street food culture.",
        },
        {
          name: "Turkey",
          code: "TR",
          image: require('@/assets/countries/turkey.jpg'),
          description:
            "Turkey bridges Europe and Asia, offering ancient ruins, vibrant bazaars, and stunning coastlines.",
        },
        {
          name: "Australia",
          code: "AU",
          image: require('@/assets/countries/australia.jpg'),
          description:
            "Australia is famous for its outback adventures, Great Barrier Reef, and cosmopolitan cities like Sydney.",
        },
        {
          name: "Brazil",
          code: "BR",
          image:  require('@/assets/countries/brazil.jpg'),
          description:
            "Brazil is home to the Amazon rainforest, the vibrant Carnival festival, and iconic landmarks like Christ the Redeemer.",
        },
        {
          name: "Canada",
          code: "CA",
          image: require('@/assets/countries/canada.jpg'),
          description:
            "Canada offers breathtaking landscapes, from the Rocky Mountains to Niagara Falls, and diverse cities.",
        },
        {
          name: "India",
          code: "IN",
          image: require('@/assets/countries/india.jpg'),
          description:
            "India is a land of contrasts, known for its ancient temples, bustling cities, and the majestic Taj Mahal.",
        },
        {
          name: "South Africa",
          code: "ZA",
          image: require('@/assets/countries/south_africa.jpg'),
          description:
            "South Africa offers diverse wildlife, beautiful landscapes, and vibrant cities like Cape Town.",
        },
        {
          name: "Russia",
          code: "RU",
          image: require('@/assets/countries/russia.jpg'),
          description:
            "Russia, the largest country in the world, is known for its grand palaces, vast wilderness, and rich history.",
        },
        {
          name: "Argentina",
          code: "AR",
          image: require('@/assets/countries/argentina.jpg'),
          description:
            "Argentina is famous for its tango, vast pampas, and breathtaking Patagonia region.",
        },
        {
          name: "Netherlands",
          code: "NL",
          image: require('@/assets/countries/netherlands.jpg'),
          description:
            "The Netherlands is known for its picturesque canals, tulip fields, and windmills.",
        },
        {
          name: "Greece",
          code: "GR",
          image: require('@/assets/countries/greece.jpg'),
          description:
            "Greece is the birthplace of democracy, known for its ancient ruins, crystal-clear waters, and islands.",
        },
        {
          name: "Malaysia",
          code: "MY",
          image: require('@/assets/countries/malaysia.jpg'),
          description:
            "Malaysia offers a mix of modern cities, lush rainforests, and stunning beaches.",
        },
        {
          name: "Egypt",
          code: "EG",
          image: require('@/assets/countries/egypt.jpg'),
          description:
            "Egypt is the land of the pharaohs, with awe-inspiring pyramids, temples, and the Nile River.",
        },
        {
          name: "Switzerland",
          code: "CH",
          image: require('@/assets/countries/switzerland.jpg'),
          description:
            "Switzerland is renowned for its alpine scenery, luxury watches, and delicious chocolates.",
        },
        {
          name: "Indonesia",
          code: "ID",
          image: require('@/assets/countries/indonesia.jpg'),
          description:
            "Indonesia, an archipelago of over 17,000 islands, offers diverse cultures, volcanoes, and beautiful beaches.",
        },
        {
          name: "Portugal",
          code: "PT",
          place: "Lagos",
          image: require('@/assets/countries/portugal.jpg'),
          description:
            "Portugal is known for its stunning coastlines, historic cities like Lisbon, and world-class wine.",
        },
        {
          name: "Austria",
          code: "AT",
          image: require('@/assets/countries/austria.jpg'),
          description:
            "Austria is celebrated for its alpine landscapes, classical music heritage, and charming cities like Vienna.",
        },
        {
          name: "Sweden",
          code: "SE",
          image: require('@/assets/countries/sweden.jpg'),
          description:
            "Sweden is known for its innovative design, lush forests, and the picturesque city of Stockholm.",
        },
        {
          name: "Vietnam",
          code: "VN",
          place: "Hanoi",
          image: require('@/assets/countries/vietnam.jpg'),
          description:
            "Vietnam is a Southeast Asian gem, famous for its vibrant street markets, stunning coastlines, and history.",
        },
        {
          name: "Singapore",
          code: "SG",
          place: "Singapore",
          image: require('@/assets/countries/singapore.jpg'),
          description:
            "Singapore is a modern city-state known for its futuristic architecture, diverse cuisine, and clean streets.",
        },
        {
          name: "New Zealand",
          code: "NZ",
          image:
            "https://images.unsplash.com/photo-1526150910403-b654f98e8100?crop=entropy&cs=tinysrgb&w=600",
          description:
            "New Zealand is a natural wonder, offering majestic mountains, serene lakes, and vibrant Maori culture.",
        },
        {
          name: "Poland",
          code: "PL",
          image:
            "https://images.unsplash.com/photo-1590608897129-79f8511a8b2a?crop=entropy&cs=tinysrgb&w=600",
          description:
            "Poland is a country rich in history, with medieval castles, Gothic cathedrals, and the bustling city of Warsaw.",
        },
        {
          name: "Morocco",
          code: "MA",
          image:
            "https://images.unsplash.com/photo-1560691657-e02a74278c1c?crop=entropy&cs=tinysrgb&w=600",
          description:
            "Morocco offers exotic souks, vast deserts, and the vibrant colors of Marrakech.",
        },
        {
          name: "Philippines",
          code: "PH",
          image:
            "https://images.unsplash.com/photo-1585736289826-87f2914cfcfd?crop=entropy&cs=tinysrgb&w=600",
          description:
            "The Philippines is a tropical paradise, known for its white-sand beaches and crystal-clear waters.",
        },
        {
          name: "Chile",
          code: "CL",
          image:
            "https://images.unsplash.com/photo-1505714197103-36ba0c18666b?crop=entropy&cs=tinysrgb&w=600",
          description:
            "Chile stretches along the Andes and offers diverse climates, from deserts to glaciers.",
        },
        {
          name: "South Korea",
          code: "KR",
          image:
            "https://images.unsplash.com/photo-1534320581557-e4fd56c6d1af?crop=entropy&cs=tinysrgb&w=600",
          description:
            "South Korea is a fascinating blend of ancient temples, bustling cities, and cutting-edge technology.",
        },
        {
          name: "United Arab Emirates",
          code: "AE",
          image:
            "https://images.unsplash.com/photo-1577627012440-ea572b776475?crop=entropy&cs=tinysrgb&w=600",
          description:
            "The UAE is known for its luxury, with futuristic cities like Dubai and the vast Arabian desert.",
        },
        {
          name: "Czech Republic",
          code: "CZ",
          image:
            "https://images.unsplash.com/photo-1562084081-4d711d6c01d4?crop=entropy&cs=tinysrgb&w=600",
          description:
            "The Czech Republic is famous for its medieval towns, Gothic architecture, and Prague's historic charm.",
        },
        {
          name: "Saudi Arabia",
          code: "SA",
          image:
            "https://images.unsplash.com/photo-1536530606091-46c7dc6b5dd4?crop=entropy&cs=tinysrgb&w=600",
          description:
            "Saudi Arabia is home to both the birthplace of Islam and stunning desert landscapes.",
        },
        {
          name: "Belgium",
          code: "BE",
          image:
            "https://images.unsplash.com/photo-1571058628229-bc482dbb8593?crop=entropy&cs=tinysrgb&w=600",
          description:
            "Belgium is known for its medieval towns, Renaissance architecture, and delicious chocolates.",
        },
        {
          name: "Israel",
          code: "IL",
          image:
            "https://images.unsplash.com/photo-1574730365990-1074ba58259d?crop=entropy&cs=tinysrgb&w=600",
          description:
            "Israel is a sacred land for many religions, with historical sites in Jerusalem and modern cities like Tel Aviv.",
        },
        {
          name: "Peru",
          code: "PE",
          image:
            "https://images.unsplash.com/photo-1529070538774-1843cb3265df?crop=entropy&cs=tinysrgb&w=600",
          description:
            "Peru is famous for Machu Picchu, ancient Inca history, and stunning Andean landscapes.",
        },
        {
          name: "Norway",
          code: "NO",
          image:
            "https://images.unsplash.com/photo-1577618998188-71cbf7e539d3?crop=entropy&cs=tinysrgb&w=600",
          description:
            "Norway is a land of fjords, northern lights, and pristine wilderness, perfect for outdoor enthusiasts.",
        },
        {
          name: "Denmark",
          code: "DK",
          image:
            "https://images.unsplash.com/photo-1551710493-2cdeb2aa7b26?crop=entropy&cs=tinysrgb&w=600",
          description:
            "Denmark is known for its charming cities, innovative design, and Viking history.",
        },
        {
          name: "Hungary",
          code: "HU",
          image:
            "https://images.unsplash.com/photo-1576060340513-9f20574e152d?crop=entropy&cs=tinysrgb&w=600",
          description:
            "Hungary is a land of thermal baths, Gothic architecture, and the beautiful capital of Budapest.",
        },
        {
          name: "Ireland",
          code: "IE",
          image:
            "https://images.unsplash.com/photo-1554568216-9459cd0a6b51?crop=entropy&cs=tinysrgb&w=600",
          description:
            "Ireland is known for its lush green landscapes, rich folklore, and historic cities like Dublin.",
        },
        {
          name: "Finland",
          code: "FI",
          image:
            "https://images.unsplash.com/photo-1532153516-59f3559f5b0e?crop=entropy&cs=tinysrgb&w=600",
          description:
            "Finland is famous for its thousands of lakes, northern lights, and cutting-edge technology.",
        },
        {
          name: "Colombia",
          code: "CO",
          image:
            "https://images.unsplash.com/photo-1560963689-b482552c3e8d?crop=entropy&cs=tinysrgb&w=600",
          description:
            "Colombia offers a diverse range of attractions, from coffee plantations to vibrant cities like Bogotá.",
        },
        {
          name: "Ukraine",
          code: "UA",
          image:
            "https://images.unsplash.com/photo-1577102594603-5fe022b060e5?crop=entropy&cs=tinysrgb&w=600",
          description:
            "Ukraine is a country of rich history and beautiful landscapes, with Kyiv's stunning cathedrals and ancient sites.",
        },
      ],
    };
  },
  methods: {
    getRegion(country) {
      const regions = {
        "France": "Europe",
        "Italy": "Europe",
        "Japan": "Asia",
        "United States": "North America",
        "Spain": "Europe",
        "China": "Asia",
        "Mexico": "North America",
        "United Kingdom": "Europe",
        "Germany": "Europe",
        "Thailand": "Asia",
        "Turkey": "Asia/Europe",
        "Australia": "Oceania",
        "Brazil": "South America",
        "Canada": "North America",
        "India": "Asia",
        "South Africa": "Africa",
        "Russia": "Europe/Asia",
        "Argentina": "South America",
        "Netherlands": "Europe",
        "Greece": "Europe",
        "Malaysia": "Asia",
        "Egypt": "Africa",
        "Switzerland": "Europe",
        "Indonesia": "Asia",
        "Portugal": "Europe",
        "Austria": "Europe",
        "Sweden": "Europe",
        "Vietnam": "Asia",
        "Singapore": "Asia",
        "New Zealand": "Oceania",
        "Poland": "Europe",
        "Morocco": "Africa",
        "Philippines": "Asia",
        "Chile": "South America",
        "South Korea": "Asia",
        "United Arab Emirates": "Asia",
        "Czech Republic": "Europe",
        "Saudi Arabia": "Asia",
        "Belgium": "Europe",
        "Israel": "Asia",
        "Peru": "South America",
        "Norway": "Europe",
        "Denmark": "Europe",
        "Hungary": "Europe",
        "Ireland": "Europe",
        "Finland": "Europe",
        "Colombia": "South America",
        "Ukraine": "Europe",
      };
      return regions[country] || "Unknown";
    },

    goToDestinationDetails(countryName) {
      this.$router.push({
        name: "DestinationDetails",
        params: { country: countryName },
      });
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

body {
  background-color: #f0f6ff;
}

/*====== HEADER ======*/

header {
  position: relative;
  overflow: hidden;
  height: 60vh; /* Adjust the height as needed */
}

.header_image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("https://images.pexels.com/photos/1271619/pexels-photo-1271619.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1");
  background-size: cover;
  background-position: center;
  z-index: -1; /* Ensures the image stays behind the content */
}

.header_container {
  position: absolute;
  bottom: 20px;
  left: 50px;
  z-index: 1;
  text-align: left;
  color: white;
}

header .content h1 {
  font-size: 3.5rem;
  font-weight: 700;
}

header content h4 {
  color: hsl(0, 0%, 70%);
  font-size: 1.5rem;
  font-weight: 500;
}

/*====== SECONDARY HEADER ======*/

.secondary_header {
  position: relative;
  left: 50px;
  top: 60px;
  
  
}

.secondary_content h5{
  color: rgb(166, 163, 163);
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
}

.card_img {
  width: 328px;
  height: 400px;
  border-radius: 1.5rem;
}

/* Text overlay styling */
.text_overlay {
  position: absolute;
  top: 10px; /* Position at the top */
  left: 10px; /* Position at the left */
  color: white; /* Text color */
  background-color: rgba(0, 0, 0, 0.2); /* Semi-transparent background */
  font-weight: bold; /* Make the text bold for readability */
  padding: 5px 10px;
  border-radius: 1rem;
  font-size: 1.2rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8); /* Adds a shadow to make the text pop */
  z-index: 10;
}

/* Optional: Add an outline (stroke) effect to the text */
.text_overlay_outline {
  -webkit-text-stroke: 1px black; /* Adds a 1px black outline around the text */
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
  text-decoration: none;
  font-size: small;
  font-weight: 500;
  color: blue;
}

.country_description {
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.5rem;
}

.card_button:hover {
  text-decoration: underline;
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
    transform: translateY(5rem);
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

/*====== BREAKPOINTS ======*/

@media screen and (max-width: 340px) {
  .container {
    margin-inline: 1rem;
  }

  .card_data {
    width: 250px;
    padding: 1rem;
  }
}

@media screen and (min-width: 768px) {
  .card_container {
    grid-template-columns: repeat(2, 1fr);
    column-gap: 1.5rem;
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
}
</style>
