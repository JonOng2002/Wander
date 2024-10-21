<template>
    <div class="about-page">
        <header class="header">
            <h1>About Wander</h1>
            <p>Your go-to app for creating personalized travel itineraries from TikTok videos.</p>
        </header>

        <section class="mission">
            <h2>Our Mission</h2>
            <p>
                At Wander, we believe in transforming travel inspiration into unforgettable experiences. Our mission is to empower travelers by providing a seamless way to gather insights and create itineraries based on the vibrant world of TikTok videos.
            </p>
        </section>

        <section class="team">
            <h2>Meet Our Team</h2>
            <div class="team-members">
                <div class="team-member">
                    <img src="../assets/team-member1.jpg" alt="Team Member 1" />
                    <h3>Jane Doe</h3>
                    <p>Co-founder & CEO</p>
                </div>
                <div class="team-member">
                    <img src="../assets/team-member2.jpg" alt="Team Member 2" />
                    <h3>John Smith</h3>
                    <p>Co-founder & CTO</p>
                </div>
                <div class="team-member">
                    <img src="../assets/team-member3.jpg" alt="Team Member 3" />
                    <h3>Alice Johnson</h3>
                    <p>Marketing Specialist</p>
                </div>
            </div>
        </section>

        <section class="faq">
            <h2>Frequently Asked Questions</h2>
            <div class="faq-item">
                <h3>How does Wander work?</h3>
                <p>Wander analyzes TikTok videos to extract travel-related insights, allowing you to create personalized itineraries.</p>
            </div>
            <div class="faq-item">
                <h3>Is there a mobile app available?</h3>
                <p>Yes! Wander is available on both iOS and Android for easy access on the go.</p>
            </div>
            <div class="faq-item">
                <h3>Can I save my itineraries?</h3>
                <p>Absolutely! You can save, edit, and share your itineraries within the app.</p>
            </div>
        </section>

        <footer class="footer">
            <p>&copy; 2024 Wander. All rights reserved.</p>
        </footer>
    </div>
</template>

<script>
export default {
    name: 'AboutPage'
}
</script>

<style scoped>
.about-page {
    font-family: Arial, sans-serif;
    color: #333; /* Dark grey for text */
    background-color: #fff; /* White background */
    padding: 20px;
    line-height: 1.6; /* Improved readability */
}

.header {
    text-align: center;
    margin-bottom: 40px;
}

.header h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
}

.header p {
    font-size: 1.2rem;
    color: #666; /* Lighter grey for subtitle */
}

.mission,
.team,
.faq {
    margin-bottom: 40px;
}

h2 {
    font-size: 2rem;
    margin-bottom: 20px;
    border-bottom: 2px solid #333; /* Underline for section titles */
    padding-bottom: 10px;
}

.team-members {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap; /* Responsive layout */
}

.team-member {
    flex: 1 1 30%; /* Flex basis for three columns */
    text-align: center;
    margin: 10px;
}

.team-member img {
    width: 100%;
    height: auto;
    border-radius: 50%; /* Circular profile pictures */
    margin-bottom: 10px;
}

.faq-item {
    margin-bottom: 20px;
}

.faq-item h3 {
    font-size: 1.5rem;
    margin-bottom: 5px;
}

.footer {
    text-align: center;
    margin-top: 40px;
    font-size: 0.9rem;
    color: #666; /* Lighter grey for footer */
}
</style>
