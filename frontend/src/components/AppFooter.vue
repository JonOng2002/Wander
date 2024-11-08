<!-- Footer.vue -->
<template>
    <footer class="footer">
        <div class="footer-container">
            <!-- Main footer content -->
            <div class="footer-grid">
                <!-- Follow Us Section -->
                <div class="footer-column">
                    <h1 class="wander-logo footer-heading">wander.</h1>
                    <h6>© 2024 Wander, an SMU project</h6>
                </div>

                <!-- Popular Destinations -->
                <div class="footer-column to-hide">
                    <h3 class="footer-heading ">Popular Destinations</h3>
                    <ul class="footer-links">
                        <li><a href="#" @click.prevent="goToDestinationDetails('Greece')">Greece</a></li>
                        <li><a href="#" @click.prevent="goToDestinationDetails('Japan')">Japan</a></li>
                        <li><a href="#" @click.prevent="goToDestinationDetails('Italy')">Italy</a></li>
                        <li><a href="#" @click.prevent="goToDestinationDetails('France')">France</a></li>   
                    </ul>
                </div>

                <!-- Travel Interests -->
                <div class="footer-column to-hide">
                    <h3 class="footer-heading">Discover more</h3>
                    <ul class="footer-links">
                        <li><a href="#" @click.prevent=viewDestinations>Explore Destinations</a></li>
                        <li><a href="#" @click.prevent=viewMainPage>Extract Locations</a></li>
                        <li><a href="#" @click.prevent=goToDestinationDetails></a></li>
                        <li><a href="#" @click.prevent=viewSavedPlaces>Plan Your Trip</a></li>
                        <li><a href="#" @click.prevent=viewAbout>About Us</a></li>
                    </ul>
                </div>

                <!-- Subscribe Section -->
                <div class="footer-column">
                    <h3 class="footer-heading">Subscribe</h3>
                    <p class="subscribe-text">Get exclusive travel tips and stories!</p>
                    <div class="subscribe-form">
                        <input type="email" placeholder="Enter your email" class="subscribe-input">
                        <button class="subscribe-button">Subscribe</button>
                    </div>
                </div>
            </div>
        </div>
    </footer>
</template>

<script>
import router from '@/router';

export default {
    name: 'AppFooter',

    setup() {
        const goToDestinationDetails = (countryName) => {
            router.push({
                name: "DestinationDetails",
                params: { country: countryName },
            });
        };

        //redirecting to the itinerary when clicked
        const viewDestinations = () => {
            router.push({
                name: 'MyDestinations',
            });
        };

        const viewAbout = () => {
            router.push({
                name: 'AboutPage',
            });
        };

        //redirecting to the itinerary when clicked
        const viewSavedPlaces = () => {
            router.push({
                name: 'SavedPlaces',
            });
        };

        //redirecting to the itinerary when clicked
        const viewMainPage = () => {
            router.push({
                name: 'MainPage',
            });
        };

        return {
            goToDestinationDetails,
            viewDestinations,
            viewSavedPlaces,
            viewMainPage,
            viewAbout,
        }
    }

};




</script>

<style scoped>
/* AppFooter.vue */
.footer {
    width: 100%;
    /* Forces the footer to take up the full viewport width */
    background-color: #000;
    color: white;
    padding: 20px 0;
    text-align: center;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    /* Ensures it stays on top if there are other elements */
}


.footer-container {
    max-width: 1200px;
    margin: 0 auto;
}

.footer-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 2rem;
}

.footer-column {
    display: flex;
    flex-direction: column;
    text-align: left;
    /* Aligns text to the left */
}

.footer-heading {
    font-family: "Lobster Two", cursive;
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    color: white;
    z-index: 1;
}

.wander-logo {
    position: relative;
    top: -12px;
    font-family: 'Lobster Two', cursive;
    font-size: 3rem;
    color: white;
    margin: 0;
    z-index: 1;
}

.social-icons {
    display: flex;
    gap: 1rem;
}

.social-icon {
    color: white;
    font-size: 1.5rem;
    transition: color 0.3s ease;
}

.social-icon:hover {
    color: #4a90e2;
}

.footer-links {
    list-style: none;
    padding: 0;
    margin: 0;
}

.footer-links li {
    margin-bottom: 0.8rem;
}

.footer-links a {
    color: #fff;
    text-decoration: none;
    transition: color 0.3s ease;
    font-size: 1rem;
}

.footer-links a:hover {
    color: #4a90e2;
}

.subscribe-text {
    margin-bottom: 1rem;
    font-size: 0.9rem;
}

.subscribe-form {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.subscribe-input {
    padding: 0.8rem;
    border: 1px solid #333;
    border-radius: 4px;
    background-color: #1a1a1a;
    color: white;
}

.subscribe-button {
    padding: 0.8rem;
    background-color: #3f94a7;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.subscribe-button:hover {
    background-color: #378597;
}

/* @media (max-width: 991px) {
    .footer-grid {
        grid-template-columns: repeat(2, 1fr);
    }
} */
@media (max-width: 1260px) {
    .footer-container {
        padding: 0 40px;
    }

}


@media (max-width: 1119px) {
    .footer-container {
        padding: 0 40px;
    }

}


@media (max-width: 991px) {
    .footer-container {
        padding: 0 40px;
    }

}

@media (max-width: 768px) {
    .footer-container {
        padding: 0 40px;
    }

    .footer-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 575px) {
    .footer-grid {
        grid-template-columns: 1fr;
    }

    .to-hide {
        display: none;
    }
}
</style>
