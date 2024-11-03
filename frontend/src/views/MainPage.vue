<template>
  <div class="homepage">
    <header class="header-container">
      <!-- Fading Background Images -->
      <div class="backgrounds-container">
        <img
          class="background showing"
          src="https://images.pexels.com/photos/346885/pexels-photo-346885.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
          alt=""
        />
        <img
          class="background"
          src="https://images.pexels.com/photos/2325446/pexels-photo-2325446.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
          alt=""
        />
        <img
          class="background"
          src="https://images.pexels.com/photos/165505/pexels-photo-165505.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
          alt=""
        />
        <img
          class="background"
          src="https://images.pexels.com/photos/307008/pexels-photo-307008.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
          alt=""
        />
        <img
          class="background"
          src="https://images.pexels.com/photos/90945/pexels-photo-90945.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
          alt=""
        />
        <img
          class="background"
          src="https://images.pexels.com/photos/2166553/pexels-photo-2166553.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
          alt=""
        />
        <img
          class="background"
          src="https://images.pexels.com/photos/2104742/pexels-photo-2104742.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
          alt=""
        />
      </div>

      <!-- Overlay Content (Centered) -->
      <div class="overlay-content">
        <p class="searchBarTitle">Where would you like to wander?</p>
        <SearchBar :disabled="isLoading" @submit-Link="handleLinkSubmit" />
        <LoadingBar :isLoading="isLoading" v-if="isLoading" />
        <div v-if="errorMessage">{{ errorMessage }}</div>
      </div>
    </header>

    
  </div>
  <!-- Main content area for search results -->
  <ExtractedLocations
      v-if="
        extractedLocationsState.locationInfo &&
        extractedLocationsState.relatedPlaces
      "
      ref="extractedLocations"
      @component-mounted="scrollToExtractedLocations"
      :locationInfo="extractedLocationsState.locationInfo"
      :relatedPlaces="extractedLocationsState.relatedPlaces"
      :userId="userId"
      :savedPlaces="savedPlaces"
    />
</template>

<script>
import SearchBar from "@/components/SearchBar.vue";
import { doc, getDoc } from "firebase/firestore";
import { db, auth } from "@/main";
import { onAuthStateChanged } from "firebase/auth";
import LoadingBar from "@/components/LoadingBar.vue";
import axios from "axios";
import ExtractedLocations from "./ExtractedLocations.vue";
import { inject } from "vue";

export default {
  name: "MainPage",
  components: {
    SearchBar,
    LoadingBar,
    ExtractedLocations
  },
  setup() {
    const extractedLocationsState = inject("extractedLocationsState");
    return { extractedLocationsState };
  },
  data() {
    return {
      userId: null,
      savedPlaces: [],
      generatedItineraries: [],
      errorMessage: "",
      isLoading: false,
      tiktokLink: "",
    };
  },
  mounted() {
    window.scrollTo(0, 0);
    onAuthStateChanged(auth, async (user) => {
      if (user) {
        this.userId = user.uid;
        await this.fetchUserData();
      }
    });

    // Initialize the fading effect
    this.startBackgroundFade();
  },
  methods: {
    startBackgroundFade() {
      let headerBackgrounds = document.querySelectorAll(".background");
      let imageIndex = 0;

      function changeBackground() {
        headerBackgrounds[imageIndex].classList.remove("showing");
        imageIndex = (imageIndex + 1) % headerBackgrounds.length;
        headerBackgrounds[imageIndex].classList.add("showing");
      }

      setInterval(changeBackground, 5000);
    },

    handleLinkSubmit(link) {
      this.tiktokLink = link;
      this.analyse();
    },

    scrollToExtractedLocations() {
    this.$nextTick(() => {
      const extractedLocationsComponent = this.$refs.extractedLocations;
      if (
        extractedLocationsComponent &&
        extractedLocationsComponent.$refs.extractedLocationsRoot
      ) {
        const extractedLocationsElement =
          extractedLocationsComponent.$refs.extractedLocationsRoot;

        if (extractedLocationsElement instanceof HTMLElement) {
          extractedLocationsElement.scrollIntoView({
            behavior: 'smooth',
            block: 'start',
          });
        } else {
          console.warn(
            'extractedLocationsElement is not an HTMLElement. Actual value:',
            extractedLocationsElement
          );
        }
      } else {
        console.warn(
          'extractedLocationsComponent or its root element is not available'
        );
      }
    });
  },

  async analyse() {
    if (this.isValidUrl(this.tiktokLink)) {
      this.isLoading = true;
      this.errorMessage = "";
      try {
        const response = await axios.get(
          `https://wander-backend-app-461191603321.asia-southeast1.run.app/video-info-comments`,
          {
            params: { url: this.tiktokLink, withCredentials: true },
          }
        );
        const data = response.data.openai_response;
        if (data.error)
          throw new Error("Error generating response from OpenAI.");
        this.extractedLocationsState.setLocationInfo(data.location_info);
        this.extractedLocationsState.setRelatedPlaces(data.related_places);
      } catch (error) {
        this.errorMessage = "Error generating response from OpenAI.";
      } finally {
        this.isLoading = false;
      }
    } else {
      this.errorMessage = "Invalid TikTok link. Please try again.";
    }
  },

    isValidUrl(url) {
      const regex =
        /^(https?:\/\/)?(www\.)?(tiktok\.com\/(@[\w.-]+\/video\/\d+)|(vt\.tiktok\.com\/[\w\d]+)).*$/;
      return regex.test(url);
    },

    async fetchUserData() {
      try {
        const userRef = doc(db, "users", this.userId);
        const userDoc = await getDoc(userRef);
        if (userDoc.exists()) {
          const userData = userDoc.data();
          this.savedPlaces = userData.savedPlaces || [];
          this.generatedItineraries = userData.generatedItineraries || [];
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    },
  },
};
</script>

<style scoped>

html, body {
  padding: 0;
  overflow-y: hidden;
  height: 100%;
  width: 100%;
}


.homepage {
  text-align: center;
  padding: 0;
  height: 100vh;
  overflow: hidden;
}

.header-container {
  height: 100vh;
  width: 100vw;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.backgrounds-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  z-index: -5;
}

.backgrounds-container::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Black with 50% opacity */
  z-index: -4; /* Places the overlay above the images but below the content */
}

.background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  object-fit: cover;
  opacity: 0;
  transition: opacity 2s ease-in-out;
}

.showing {
  opacity: 1;
  z-index: -1;
  transition: none;
}

.overlay-content {
  position: absolute;
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 10rem;
  width: 100%;           /* Ensures full-width overlay content */
  max-width: 100vw;      /* Prevents any padding from restricting width */
  text-align: center;
  z-index: 1;
}

h1,
p {
  color: white;
  margin: 0;
  padding: 0;
}

.searchBarTitle {
  display: block;         /* Ensures full-width for the title row */
  font-size: 4rem;
  margin: 20px 0;
  font-weight: bold;
  color: white;
  width: 100%;            /* Expands to fill the width of the container */
  text-align: center;     /* Centers text within the full-width row */
}

</style>
