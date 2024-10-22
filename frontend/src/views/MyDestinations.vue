<template>
  <div class="my-destinations">
    <h1>Wander the World: Top Must-Visit Locations</h1>

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
h1 {
  font-family: 'Cormorant Garamond', serif;
  font-weight: bolder;
  margin-bottom: 20px;
  color: #2c3e50; /* Darker color for better contrast */
  font-size: 3rem;
}

.my-destinations {
  text-align: center;
  font-family: "Roboto", sans-serif;
  padding: 20px; /* Padding for overall spacing */
}

.countries-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); /* Responsive grid */
  gap: 20px; /* Space between cards */
}

.country-card {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background: white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* Soft shadow for depth */
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* Smooth transitions */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 300px; /* Consistent height */
}

.country-card:hover {
  transform: translateY(-5px); /* Lift effect on hover */
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4); /* Enhanced shadow with darker effect */
}


.country-card h2 {
  font-size: 1.3rem;
  margin: 10px 0;
  color: #34495e; /* Slightly lighter text color */
}

.country-card img {
  width: 100%;
  height: 150px; /* Fixed height for consistency */
  object-fit: cover;
  border-radius: 5px; /* Rounded corners for images */
}

.country-card button {
  margin-top: 10px;
  background-color: black; /* Brand color for buttons */
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.country-card button:hover {
  background-color: #333;
}
</style>
