<template>
  <ul class="nav flex-column contentbar">
    <li class="nav-item">
      <a class="nav-link active" href="#mtfuji">Mt Fuji</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" href="#tokyotower">Tokyo Tower</a>
    </li>
  </ul>

  <h3>Extracted locations</h3>

  <div class="card mx-auto mb-5" style="width: 40rem;">
    <img id="mtfuji" src="../assets/mountfuji.png" class="card-img-top" alt="...">
    <div class="card-body pb-0">
      <h5 class="card-title">Mt Fuji</h5>
      <p class="card-text">Standing at 3,776 meters, Mt. Fuji is the tallest peak in Japan, the result of volcanic
        activity that began approximately 100,000 years ago. Today, Mt. Fuji and the surrounding area are a popular
        recreational destination for hiking, camping and relaxation.</p>
    </div>
    <hr>
    <div class="card-body py-0">
      <h5 class="card-title">Location</h5>
      <ul class="list-group list-group-flush">
        <li class="list-group-item">Kitayama, Fujinomiya, Shizuoka 418-0112, Japan</li>
      </ul>
      <!-- Map container for Mt Fuji -->
      <div id="mtfuji-map" class="map"></div>
    </div>
    <hr>
    <div class="card-body pt-0">
      <button class="btn btn-dark">Add to saved places</button>
      
    </div>
  </div>

  <div class="card mx-auto" style="width: 40rem;">
    <img id="tokyotower" src="../assets/tokyotower.jpg" class="card-img-top" alt="...">
    <div class="card-body pb-0">
      <h5 class="card-title">Tokyo Tower</h5>
      <p class="card-text">Standing 333 meters high in central Tokyo, Tokyo Tower (東京タワー) is the world's tallest,
        self-supported steel tower and 3 meters taller than its model, the Eiffel Tower. A symbol of Japan's post-war
        rebirth as a major economic power, Tokyo Tower was the country's tallest structure from its completion in 1958
        until 2012 when it was surpassed by the Tokyo Skytree</p>
    </div>
    <hr>
    <div class="card-body py-0">
      <h5 class="card-title">Location</h5>
      <ul class="list-group list-group-flush">
        <li class="list-group-item">4 Chome-2-8 Shibakoen, Minato City, Tokyo 105-0011, Japan</li>
      </ul>
      <!-- Map container for Tokyo Tower -->
      <div id="tokyotower-map" class="map"></div>
    </div>
    <hr>
    <div class="card-body pt-0">
      <button class="btn btn-dark">Add to saved places</button>
      
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExtractedLocations',
  mounted() {
    // Initialize Mt. Fuji Map
    this.initMap('mtfuji-map', { lat: 35.3606, lng: 138.7274 });

    // Initialize Tokyo Tower Map
    this.initMap('tokyotower-map', { lat: 35.6586, lng: 139.7454 });
  },
  methods: {
    // Method to initialize the Google Map
    initMap(mapId, coordinates) {
      const map = new google.maps.Map(document.getElementById(mapId), {
        center: coordinates,
        zoom: 12,
      });

      // Marker for the specific location
      new google.maps.Marker({
        position: coordinates,
        map: map,
      });
    },
  },
};
</script>

<style scoped>
.card-img-top {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.contentbar {
  position: fixed;
  border: 1px solid black;
  margin: 10px;
}

h3 {
  text-align: center;
  font-family: 'Times New Roman', Times, serif;
  margin: 10px 0px;
  font-weight: bold;
  font-size: 40px;
}

.map {
  height: 300px;
  width: 100%;
}
</style>
