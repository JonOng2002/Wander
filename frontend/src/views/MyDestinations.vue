<template>
  <div class="my-destinations">
    <h1>Top Destinations for Wanderers</h1>

    <!-- List of countries -->
    <div class="countries-list">
      <div
        v-for="country in countries"
        :key="country.code"
        class="country-card"
      >
        <img :src="country.flag" alt="country-flag" class="country-flag" />
        <h2>{{ country.name }}</h2>
        <button @click="goToCountry(country.name)" class="btn">
          View Top Attractions
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MyDestinations",
  data() {
    return {
      // Static list of top 20 tourist countries
      countries: [
        { name: "France", code: "FR", flag: "https://flagcdn.com/w320/fr.png" },
        { name: "Italy", code: "IT", flag: "https://flagcdn.com/w320/it.png" },
        { name: "Japan", code: "JP", flag: "https://flagcdn.com/w320/jp.png" },
        {
          name: "United States",
          code: "US",
          flag: "https://flagcdn.com/w320/us.png",
        },
        { name: "Spain", code: "ES", flag: "https://flagcdn.com/w320/es.png" },
        { name: "China", code: "CN", flag: "https://flagcdn.com/w320/cn.png" },
        { name: "Mexico", code: "MX", flag: "https://flagcdn.com/w320/mx.png" },
        {
          name: "United Kingdom",
          code: "GB",
          flag: "https://flagcdn.com/w320/gb.png",
        },
        {
          name: "Germany",
          code: "DE",
          flag: "https://flagcdn.com/w320/de.png",
        },
        {
          name: "Thailand",
          code: "TH",
          flag: "https://flagcdn.com/w320/th.png",
        },
        { name: "Turkey", code: "TR", flag: "https://flagcdn.com/w320/tr.png" },
        {
          name: "Australia",
          code: "AU",
          flag: "https://flagcdn.com/w320/au.png",
        },
        { name: "Brazil", code: "BR", flag: "https://flagcdn.com/w320/br.png" },
        { name: "Canada", code: "CA", flag: "https://flagcdn.com/w320/ca.png" },
        { name: "India", code: "IN", flag: "https://flagcdn.com/w320/in.png" },
        {
          name: "South Africa",
          code: "ZA",
          flag: "https://flagcdn.com/w320/za.png",
        },
        { name: "Russia", code: "RU", flag: "https://flagcdn.com/w320/ru.png" },
        {
          name: "Argentina",
          code: "AR",
          flag: "https://flagcdn.com/w320/ar.png",
        },
        {
          name: "Netherlands",
          code: "NL",
          flag: "https://flagcdn.com/w320/nl.png",
        },
        { name: "Greece", code: "GR", flag: "https://flagcdn.com/w320/gr.png" },
      ],
    };
  },
  methods: {
    // Navigate to the country's details page (DestinationDetails)
    goToCountry(countryName) {
      this.$router.push({
        name: "DestinationDetails",
        params: { country: countryName },
      });
    },
  },
};
</script>

<style scoped>
.my-destinations {
  text-align: center;
  font-family: "Roboto", sans-serif;
}

.countries-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.country-card {
  margin: 20px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 10px;
  width: 200px;
  text-align: center;
  transition: transform 0.3s ease;
  /* Set a fixed height for consistency */
  height: 300px; /* Adjust height to your needs */

  /* Use flexbox to center content vertically */
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  /* Ensure consistency for the text */
  overflow: hidden;
}

.country-card h2 {
  font-size: 1.2rem;
  margin-bottom: 10px;

  /* Force text to be consistent and avoid overflow */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.country-card img {
  width: 100%;
  height: auto;
  margin-bottom: 10px;
}

.country-card p {
  flex-grow: 1; /* Take up remaining space */
}

.country-card button {
  margin-top: auto;
}


.country-card:hover {
  transform: scale(1.05);
}

.country-flag {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 5px;
  margin-bottom: 10px;
}

.btn {
  background-color: lightgray;
  color: black;
  border: 1px solid black;
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: bold;
  font-family: "Roboto", sans-serif;
  text-transform: uppercase;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: darkgray;
}

button {
  margin-top: 10px;
}

h1 {
  margin-top: 20px;
}
</style>
