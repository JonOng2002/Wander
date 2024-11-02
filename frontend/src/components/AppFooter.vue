<!-- Footer.vue -->
<template>
    <footer class="footer">
        <div class="footer-content">
            <p>© 2024 Company Name. All rights reserved.</p>
            <nav class="footer-links">
                <a href="#">Terms of Use</a>
                <a href="#">Privacy Policy</a>
                <a href="#">Contact Us</a>
            </nav>
            <div class="footer-options">
                <select>
                    <option>$ SGD</option>
                    <option>$ USD</option>
                    <option>€ EUR</option>
                </select>
                <select>
                    <option>Singapore</option>
                    <option>United States</option>
                    <option>Europe</option>
                </select>
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
.footer {
    background-color: #e0e0e0; /* Gray background */
    width: 100%;
    padding: 20px;
    text-align: center;
    margin-top: 100px; /* Adds 100px margin from the nearest item above */
}

.footer-content {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
}

.footer-links {
    display: flex;
    gap: 15px;
}

.footer-links a {
    color: #000;
    text-decoration: none;
    margin: 0 10px;
}

.footer-links a:hover {
    text-decoration: underline;
}

.footer-options select {
    margin: 0 5px;
    padding: 5px;
}
</style>
