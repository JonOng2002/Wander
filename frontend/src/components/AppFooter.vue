<!-- Footer.vue -->
<template>
    <footer class="footer">
        <div class="footer-container">
                <!-- Main footer content -->
                <div class="footer-grid">
                    <!-- Follow Us Section -->
                    <div class="footer-column">
                        <h3 class="footer-heading">Follow Us</h3>
                        <div class="social-icons">
                            <a href="#" class="social-icon">
                                <i class="fab fa-facebook"></i>
                            </a>
                            <a href="#" class="social-icon">
                                <i class="fab fa-instagram"></i>
                            </a>
                            <a href="#" class="social-icon">
                                <i class="fab fa-tiktok"></i>
                            </a>
                            <a href="#" class="social-icon">
                                <i class="fab fa-youtube"></i>
                            </a>
                        </div>
                    </div>

                    <!-- Popular Destinations -->
                    <div class="footer-column">
                        <h3 class="footer-heading">Popular Destinations</h3>
                        <ul class="footer-links">
                            <li><a href="#">Bali</a></li>
                            <li><a href="#">Greece</a></li>
                            <li><a href="#">Japan</a></li>
                            <li><a href="#">Italy</a></li>
                            <li><a href="#">France</a></li>
                        </ul>
                    </div>

                    <!-- Travel Interests -->
                    <div class="footer-column">
                        <h3 class="footer-heading">Travel Interests</h3>
                        <ul class="footer-links">
                            <li><a href="#">Adventure Travel</a></li>
                            <li><a href="#">Cultural Tours</a></li>
                            <li><a href="#">Beach Getaways</a></li>
                            <li><a href="#">City Breaks</a></li>
                            <li><a href="#">Food & Wine</a></li>
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
export default {
    name: 'AppFooter',
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
    margin-top: 50px;
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
    text-align: left; /* Aligns text to the left */
}

.footer-heading {
    font-family: "Lobster Two", cursive;
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    color: white;
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
    background-color: #4a90e2;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.subscribe-button:hover {
    background-color: #357abd;
}

@media (max-width: 768px) {
    .footer-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 480px) {
    .footer-grid {
        grid-template-columns: 1fr;
    }
}
</style>
