<template>
    <div class="about">
        <div class="image-container">
            <img src="../assets/landingpage.jpg" alt="Wander Thumbnail" class="thumbnail" />
            <div class="overlay">
                <h1>Welcome to Wander!</h1>
                <p>This app allows you to analyze TikTok videos and gather insights for your itineraries.</p>
                <p>Feel free to explore the various features and functionalities.</p>
                <button class="button-75" @click="handleGetStarted"><span class="text">Get Started</span></button>
            </div>
        </div>
    </div>
</template>

<script>
import { useRouter } from 'vue-router';

export default {
    name: 'AboutPage',
    setup() {
        const router = useRouter();

        const handleGetStarted = () => {
            router.push('/');
        };

        return {
            handleGetStarted
        };
    }
}
</script>

<style scoped>
.about {
    position: relative; /* Ensure proper positioning of the overlay */
    text-align: center;
}

.image-container {
    position: relative;
    width: 100%;
    height: 100vh; /* Set height to full viewport */
    overflow: hidden; /* Hide overflow */
}

.thumbnail {
    width: 100%;
    height: 100%; /* Cover full height */
    object-fit: cover; /* Ensure image covers the area */
}

.overlay {
    position: absolute; /* Position overlay relative to container */
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%); /* Center the overlay */
    color: white; /* Set text color to white for contrast */
    text-align: center; /* Center the text */
    background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
    padding: 20px;
    border-radius: 10px; /* Rounded corners for a softer look */
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}

h1 {
    font-size: 2.5rem;
    margin-bottom: 20px;
}

p {
    font-size: 1.2rem;
    line-height: 1.6; /* Improve readability */
    align-items: center;
}

.button-75 {
    align-items: center;
    background-image: linear-gradient(135deg, #f34079 40%, #fc894d);
    border: 0;
    border-radius: 10px;
    box-sizing: border-box;
    color: #fff;
    cursor: pointer;
    font-family: "Codec cold", sans-serif;
    font-size: 16px;
    font-weight: 700;
    height: 54px;
    justify-content: center;
    letter-spacing: .4px;
    line-height: 1;
    max-width: 50%;
    padding-left: 20px;
    padding-right: 20px;
    padding-top: 3px;
    text-decoration: none;
    text-transform: uppercase;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
    justify-content: center;
}

.button-75:hover {
    outline: 0;
}

.button-75 span {
    transition: all 200ms;
}

.button-75:hover span {
    transform: scale(.9);
    opacity: .75;
}
</style>