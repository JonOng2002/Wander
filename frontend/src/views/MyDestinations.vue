<template>
  <div class="my-destinations">
    <h1>Wander the World: Top Must-Visit Locations</h1>

    <!-- List of countries -->
    <div class="row countries-list" @scroll.passive="onScroll">
      <div
        v-for="(country, index) in countries"
        :key="country.code"
        class="col-md-4 col-sm-6 col-xs-12 country-card"
      >
        <div class="image-container">
          <div class="overlay">
            <span class="number">{{ index + 1 }}</span>
          </div>
          <img :src="country.flag.replace('w320', 'w160')" alt="country-flag" class="country-image" loading="lazy" />
        </div>
        <div class="card-details">
          <h2 class="country-name">{{ country.name }}</h2>
          <p class="country-region">{{ getRegion(country.name) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MyDestinations",
  data() {
    return {
      countries: [
        { name: "France", code: "FR", flag: "https://flagcdn.com/w320/fr.png" },
        { name: "Italy", code: "IT", flag: "https://flagcdn.com/w320/it.png" },
        { name: "Japan", code: "JP", flag: "https://flagcdn.com/w320/jp.png" },
        { name: "United States", code: "US", flag: "https://flagcdn.com/w320/us.png" },
        { name: "Spain", code: "ES", flag: "https://flagcdn.com/w320/es.png" },
        { name: "China", code: "CN", flag: "https://flagcdn.com/w320/cn.png" },
        { name: "Mexico", code: "MX", flag: "https://flagcdn.com/w320/mx.png" },
        { name: "United Kingdom", code: "GB", flag: "https://flagcdn.com/w320/gb.png" },
        { name: "Germany", code: "DE", flag: "https://flagcdn.com/w320/de.png" },
        { name: "Thailand", code: "TH", flag: "https://flagcdn.com/w320/th.png" },
        { name: "Turkey", code: "TR", flag: "https://flagcdn.com/w320/tr.png" },
        { name: "Australia", code: "AU", flag: "https://flagcdn.com/w320/au.png" },
        { name: "Brazil", code: "BR", flag: "https://flagcdn.com/w320/br.png" },
        { name: "Canada", code: "CA", flag: "https://flagcdn.com/w320/ca.png" },
        { name: "India", code: "IN", flag: "https://flagcdn.com/w320/in.png" },
        { name: "South Africa", code: "ZA", flag: "https://flagcdn.com/w320/za.png" },
        { name: "Russia", code: "RU", flag: "https://flagcdn.com/w320/ru.png" },
        { name: "Argentina", code: "AR", flag: "https://flagcdn.com/w320/ar.png" },
        { name: "Netherlands", code: "NL", flag: "https://flagcdn.com/w320/nl.png" },
        { name: "Greece", code: "GR", flag: "https://flagcdn.com/w320/gr.png" },
        { name: "Malaysia", code: "MY", flag: "https://flagcdn.com/w320/my.png" },
        { name: "Egypt", code: "EG", flag: "https://flagcdn.com/w320/eg.png" },
        { name: "Switzerland", code: "CH", flag: "https://flagcdn.com/w320/ch.png" },
        { name: "Indonesia", code: "ID", flag: "https://flagcdn.com/w320/id.png" },
        { name: "Portugal", code: "PT", flag: "https://flagcdn.com/w320/pt.png" },
        { name: "Austria", code: "AT", flag: "https://flagcdn.com/w320/at.png" },
        { name: "Sweden", code: "SE", flag: "https://flagcdn.com/w320/se.png" },
        { name: "Vietnam", code: "VN", flag: "https://flagcdn.com/w320/vn.png" },
        { name: "Singapore", code: "SG", flag: "https://flagcdn.com/w320/sg.png" },
        { name: "New Zealand", code: "NZ", flag: "https://flagcdn.com/w320/nz.png" },
        { name: "Poland", code: "PL", flag: "https://flagcdn.com/w320/pl.png" },
        { name: "Morocco", code: "MA", flag: "https://flagcdn.com/w320/ma.png" },
        { name: "Philippines", code: "PH", flag: "https://flagcdn.com/w320/ph.png" },
        { name: "Chile", code: "CL", flag: "https://flagcdn.com/w320/cl.png" },
        { name: "South Korea", code: "KR", flag: "https://flagcdn.com/w320/kr.png" },
        { name: "United Arab Emirates", code: "AE", flag: "https://flagcdn.com/w320/ae.png" },
        { name: "Czech Republic", code: "CZ", flag: "https://flagcdn.com/w320/cz.png" },
        { name: "Saudi Arabia", code: "SA", flag: "https://flagcdn.com/w320/sa.png" },
        { name: "Belgium", code: "BE", flag: "https://flagcdn.com/w320/be.png" },
        { name: "Israel", code: "IL", flag: "https://flagcdn.com/w320/il.png" },
        { name: "Peru", code: "PE", flag: "https://flagcdn.com/w320/pe.png" },
        { name: "Norway", code: "NO", flag: "https://flagcdn.com/w320/no.png" },
        { name: "Denmark", code: "DK", flag: "https://flagcdn.com/w320/dk.png" },
        { name: "Hungary", code: "HU", flag: "https://flagcdn.com/w320/hu.png" },
        { name: "Ireland", code: "IE", flag: "https://flagcdn.com/w320/ie.png" },
        { name: "Finland", code: "FI", flag: "https://flagcdn.com/w320/fi.png" },
        { name: "Colombia", code: "CO", flag: "https://flagcdn.com/w320/co.png" },
        { name: "Ukraine", code: "UA", flag: "https://flagcdn.com/w320/ua.png" },
      ],
      scrollDisabled: false, // To control disabling of transitions
    };
  },
  methods: {
    getRegion(country) {
      const regions = {
        'France': 'Europe',
        'Italy': 'Europe',
        'Japan': 'Asia',
        'United States': 'North America',
        'Spain': 'Europe',
        'China': 'Asia',
        'Mexico': 'North America',
        'United Kingdom': 'Europe',
        'Germany': 'Europe',
        'Thailand': 'Asia',
        'Turkey': 'Asia/Europe',
        'Australia': 'Oceania',
        'Brazil': 'South America',
        'Canada': 'North America',
        'India': 'Asia',
        'South Africa': 'Africa',
        'Russia': 'Europe/Asia',
        'Argentina': 'South America',
        'Netherlands': 'Europe',
        'Greece': 'Europe',
        'Malaysia': 'Asia',
        'Egypt': 'Africa',
        'Switzerland': 'Europe',
        'Indonesia': 'Asia',
        'Portugal': 'Europe',
        'Austria': 'Europe',
        'Sweden': 'Europe',
        'Vietnam': 'Asia',
        'Singapore': 'Asia',
        'New Zealand': 'Oceania',
        'Poland': 'Europe',
        'Morocco': 'Africa',
        'Philippines': 'Asia',
        'Chile': 'South America',
        'South Korea': 'Asia',
        'United Arab Emirates': 'Asia',
        'Czech Republic': 'Europe',
        'Saudi Arabia': 'Asia',
        'Belgium': 'Europe',
        'Israel': 'Asia',
        'Peru': 'South America',
        'Norway': 'Europe',
        'Denmark': 'Europe',
        'Hungary': 'Europe',
        'Ireland': 'Europe',
        'Finland': 'Europe',
        'Colombia': 'South America',
        'Ukraine': 'Europe',
      };
      return regions[country] || 'Unknown';
    },
    onScroll() {
      if (!this.scrollDisabled) {
        // Disable transitions during scroll for smoother scrolling
        this.scrollDisabled = true;

        setTimeout(() => {
          this.scrollDisabled = false;
        }, 200); // Re-enable transitions after 200ms
      }
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
  margin-top: 20px;
}

.countries-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  max-height: 100vh;
  overflow-y: auto;
}

.country-card {
  margin: 20px;
  padding: 0;
  position: relative;
  width: 220px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.country-card:hover {
  transform: scale(1.03);
}

.image-container {
  position: relative;
  width: 100%;
  height: 280px;
}

.country-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
}

.overlay {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: rgba(0, 0, 0, 0.6);
  padding: 5px 10px;
  border-radius: 50%;
  color: white;
  font-weight: bold;
  font-size: 1.2rem;
}

.card-details {
  text-align: center;
  padding: 10px 0;
}

.country-name {
  font-size: 1.4rem;
  font-weight: bold;
  margin-bottom: 5px;
}

.country-region {
  color: #999;
  font-size: 1rem;
}

@media (hover: none) {
  .country-card:hover {
    transform: none;
  }
}

.country-card {
  /* Disable transitions when scrolling is active */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
</style>
