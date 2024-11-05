<template>
    <div class="loader-container">
        <div class="loader"></div>
        <div class="loading-text">{{ currentText }}</div>
    </div>
</template>

<script>
export default {
    props: {
        isLoading: {
            type: Boolean,
            required: true
        }
    },
    data() {
        return {
            texts: ["Your Ticket to Adventure is Loading...","Packing Your Bags...", "Mapping Your Journey...", "Finding Your Next Getaway...", "Jetting Off Soon... "],
            currentText: "",
            textIndex: 0
        };
    },
    mounted() {
        if (this.isLoading) {
            this.startTextAnimation();
        }
    },
    beforeUnmount() {
        clearInterval(this.textInterval); // Clear interval on component destroy
    },
    methods: {
        startTextAnimation() {
        this.currentText = this.texts[this.textIndex]; // Set initial text
        this.textInterval = setInterval(() => {
            this.textIndex++;
            // Check if the textIndex is within bounds
            if (this.textIndex < this.texts.length) {
                this.currentText = this.texts[this.textIndex]; // Update text
            } else {
                clearInterval(this.textInterval); // Clear interval when the last text is reached
            }
        }, 2400); // Change text every 2.4 seconds (2400ms)
        }
    }
}
</script>

<style scoped>
.loader-container {
    display: flex;
    flex-direction: column; /* Stack loader and text vertically */
    justify-content: center; /* Center horizontally */
    align-items: center; /* Center vertically */
    width: 100%; /* Full width */
    margin-top: 3rem;
}

.loader {
    width: calc(6 * 30px);
    height: 50px;
    display: flex;
    color: white;
    filter: drop-shadow(30px 25px 0 currentColor) drop-shadow(60px 0 0 currentColor) drop-shadow(120px 0 0 currentColor);
    clip-path: inset(0 100% 0 0);
    animation: l13 2s infinite steps(7);
    
}

.loader:before {
    content: "";
    width: 30px;
    height: 25px;
    background: 
        radial-gradient(farthest-side at right, currentColor 92%, #0000) left/20px 100% no-repeat,
        radial-gradient(farthest-side, currentColor 92%, #0000) right/17px 9px repeat-y;
}

@keyframes l13 {
    100% {clip-path: inset(0 -30px 0 0)}
}

.loading-text {
    color: white; /* Text color */
    margin-top: 1rem; /* Space between loader and text */
    font-size: 18px; /* Adjust font size */
    text-align: center; /* Center text */
    text-shadow: 1px 1px 2px black; /* Outline effect for text */
}
</style>