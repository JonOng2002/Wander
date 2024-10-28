<template>
    <div class="main-container">
        <div class="title">
            <link href="https://fonts.googleapis.com/css2?family=Lobster+Two:wght@400;700&display=swap"
                rel="stylesheet">
            <h1>wander.</h1>
        </div>
        <div ref="threeContainer" class="three-container"></div>

        <div class="main-feature">
            <div class="heading">
                <h2>Start your journey with a click!</h2>
            </div>
            <div class="destination-cards">
                <div class="card">
                    <img src="../assets/about/hongkong.jpeg" alt="Vanuatu" />
                    <p>Vanuatu</p>
                </div>
                <div class="card">
                    <img src="../assets/about/japan.jpeg" alt="Toulouse" />
                    <p>Toulouse</p>
                </div>
                <div class="card">
                    <img src="../assets/about/france.jpeg" alt="Armenia" />
                    <p>Armenia</p>
                </div>
            </div>
        </div>

        <div class="video-section" ref="videoSection">
            <p>Explore the world at your fingertips</p>
            <div class="video-container">
                <video autoplay loop muted playsinline>
                    <source src="../assets/destinations.mp4" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
        </div>

        <div class="video-section" ref="videoSection">
            <p>All your saved places at a glance</p>
            <div class="video-container">
                <video autoplay loop muted playsinline>
                    <source src="../assets/saved.mp4" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
        </div>

        <div class="carousel-section" ref="carouselSection">
            <div class="carousel-header">
                <h2>Where to next?</h2>
            </div>
            <div class="carousel-container">
                <div class="carousel-track" ref="carouselTrack">
                    <!-- Double the images for seamless loop -->
                    <div v-for="(image, index) in [...images, ...images, ...images, ...images]" :key="index"
                        class="carousel-slide">
                        <div class="image-container">
                            <img :src="image.src" :alt="image.alt || `Slide ${index + 1}`">
                            <div class="image-caption">{{ image.country }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="video-section" ref="videoSection">
            <div class="video-container">
                <video autoplay loop muted playsinline>
                    <source src="../assets/travel.mp4" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
        </div>

        <footer class="footer-section">
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
    </div>
</template>


<script>
import { onMounted, ref, router } from 'vue';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

export default {
    name: 'ThreeScene',
    data() {
        return {
            images: [
                { src: require('../assets/about/finland.jpeg'), alt: 'image1', country: 'Finland' },
                { src: require('../assets/about/switzerland.jpeg'), alt: 'image2', country: 'Switzerland' },
                { src: require('../assets/about/spain.jpeg'), alt: 'image3', country: 'Spain' },
                { src: require('../assets/about/france.jpeg'), alt: 'image4', country: 'France' },
                { src: require('../assets/about/italy.jpeg'), alt: 'image5', country: 'Italy' },
                { src: require('../assets/about/bali.jpeg'), alt: 'image5', country: 'Bali' },
                { src: require('../assets/about/korea.jpeg'), alt: 'image5', country: 'Korea' },
                { src: require('../assets/about/greece.jpeg'), alt: 'image5', country: 'Greece' },
                { src: require('../assets/about/germany.jpeg'), alt: 'image5', country: 'Germany' },
                { src: require('../assets/about/china.jpeg'), alt: 'image5', country: 'China' },
                { src: require('../assets/about/hongkong.jpeg'), alt: 'image5', country: 'Hong Kong' },
                { src: require('../assets/about/japan.jpeg'), alt: 'image5', country: 'Japan' },
            ],
            scrollInterval: null,
            scrollPosition: 0,
            scrollSpeed: 0.1, // Pixels per frame
        };
    },
    setup() {
        const threeContainer = ref(null);
        const carouselSection = ref(null);
        const carouselTrack = ref(null);
        let globe = null;
        let renderer = null;

        const setupIntersectionObserver = () => {
            const options = {
                root: null,
                rootMargin: '0px',
                threshold: [0, 0.2, 0.4, 0.6, 0.8, 1]
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.target === threeContainer.value) {
                        const opacity = entry.intersectionRatio;
                        if (globe) {
                            globe.material.opacity = opacity;
                            globe.children[0].material.opacity = opacity * 0.1;
                        }
                    }
                    if (entry.target === carouselSection.value) {
                        carouselSection.value.style.opacity = entry.intersectionRatio;
                    }
                });
            }, options);

            observer.observe(threeContainer.value);
            observer.observe(carouselSection.value);
        };

        onMounted(() => {
            if (!threeContainer.value) return;

            // Scene setup (same as before)
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(
                75,
                window.innerWidth / window.innerHeight,
                0.1,
                1000
            );
            camera.position.z = 5;

            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setClearColor(0x000000, 1);
            renderer.physicallyCorrectLights = true;
            renderer.toneMapping = THREE.ACESFilmicToneMapping;
            renderer.toneMappingExposure = 1.5;
            threeContainer.value.appendChild(renderer.domElement);

            // Controls setup (same as before)
            const controls = new OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.rotateSpeed = 0.5;
            controls.enableRotate = true;
            controls.enableZoom = false;
            controls.minDistance = 3;
            controls.maxDistance = 10;
            controls.enablePan = true;
            controls.panSpeed = 0.5;

            // Lighting (same as before)
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
            scene.add(ambientLight);

            const mainLight = new THREE.DirectionalLight(0xffffff, 2);
            mainLight.position.set(5, 3, 5);
            scene.add(mainLight);

            const rimLight = new THREE.DirectionalLight(0x9999ff, 1);
            rimLight.position.set(-5, 3, -5);
            scene.add(rimLight);

            const fillLight = new THREE.DirectionalLight(0xfff0dd, 0.5);
            fillLight.position.set(0, -5, 0);
            scene.add(fillLight);

            // Load Earth texture (same as before)
            const textureLoader = new THREE.TextureLoader();
            textureLoader.load(
                '/nasa.jpg',
                (texture) => {
                    texture.encoding = THREE.sRGBEncoding;
                    texture.anisotropy = renderer.capabilities.getMaxAnisotropy();

                    const geometry = new THREE.SphereGeometry(2, 64, 64);
                    const material = new THREE.MeshStandardMaterial({
                        map: texture,
                        roughness: 0.5,
                        metalness: 0.1,
                        envMapIntensity: 1.0,
                        transparent: true,
                        opacity: 1
                    });

                    globe = new THREE.Mesh(geometry, material);

                    const atmosphereGeometry = new THREE.SphereGeometry(2.1, 64, 64);
                    const atmosphereMaterial = new THREE.MeshPhongMaterial({
                        color: 0x4ca6ff,
                        transparent: true,
                        opacity: 0.1,
                        side: THREE.BackSide,
                    });
                    const atmosphere = new THREE.Mesh(atmosphereGeometry, atmosphereMaterial);
                    globe.add(atmosphere);

                    scene.add(globe);
                    globe.position.y = 0.8;

                    const pmremGenerator = new THREE.PMREMGenerator(renderer);
                    scene.environment = pmremGenerator.fromScene(scene).texture;

                    setupIntersectionObserver();

                    function animate() {
                        requestAnimationFrame(animate);
                        controls.minPolarAngle = Math.PI / 3;
                        controls.maxPolarAngle = Math.PI / 2;
                        controls.update();
                        renderer.render(scene, camera);
                    }

                    animate();
                },
                undefined,
                (error) => {
                    console.error('An error occurred loading the texture.', error);
                }
            );


        });

        return { threeContainer, carouselSection, carouselTrack };
    },
    mounted() {
        this.startAutoScroll();
        const video = document.querySelector('video');
        video.play().catch(function (error) {
            console.log("Video autoplay failed:", error);
        });
    },

    beforeUnmount() {
        this.stopAutoScroll();
    },
    methods: {
        startAutoScroll() {
            const animate = () => {
                if (this.carouselTrack) {
                    this.scrollPosition += this.scrollSpeed;
                    const maxScroll = this.images.length * 100; // 100% per image

                    if (this.scrollPosition >= maxScroll) {
                        this.scrollPosition = 0;
                    }

                    this.$refs.carouselTrack.style.transform = `translateX(-${this.scrollPosition}%)`;
                }
                this.scrollInterval = requestAnimationFrame(animate);
            };
            animate();
        },
        stopAutoScroll() {
            if (this.scrollInterval) {
                cancelAnimationFrame(this.scrollInterval);
            }
        },

        navigateTologin() {
            router.push({
                name: 'LogIn',
            });
        },

        navigateTosignup() {
            router.push({
                name: 'SignUp',
            });
        }
    }
};
</script>

<style>
.main-container {
    height: 200vh;
    overflow-y: auto;
    overflow-x: hidden;
    background-color: black;
    color: white;
    margin: 0;
    padding: 0;
}

.three-container {
    width: 70vw;
    height: 70vh;
    overflow: hidden;
    cursor: grab;
    /* position: sticky; */
    top: 0;
}

.title h1 {
    font-family: "Lobster Two";
    font-weight: 800;
    text-align: center;
    padding-top: 40px;
    font-size: 100px;
    width: 100%;
    z-index: 10;
}

.carousel-section {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    opacity: 0;
    transition: opacity 0.5s ease;
    padding: 2rem 0;
}

.carousel-container {
    width: 80vw;
    height: 60vh;
    position: relative;
    overflow: hidden;
    margin-top: 2rem;
}

.carousel-track {
    display: flex;
    height: 100%;
    will-change: transform;
}

.carousel-slide {
    min-width: 33.333%;
    height: 100%;
    padding: 0 10px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
}

.image-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
}

.carousel-slide img {
    width: 100%;
    height: 85%;
    object-fit: cover;
    border-radius: 10px 10px 0 0;
}

.image-caption {
    width: 100%;
    text-align: center;
    padding: 12px;
    font-size: 1.2rem;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(5px);
    border-radius: 0 0 10px 10px;
    margin-top: auto;
}

.carousel-header {
    text-align: center;
    padding: 1rem 0;
    margin-bottom: 1rem;
    margin-top: 100px;
}

.carousel-header h2 {
    font-size: 2.5rem;
    margin: 0;
    font-family: "Cormorant Garamond", serif;
    font-weight: bolder;
}

.video-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 4rem 0;
    width: 100%;
}

.video-container {
    display: flex;
    justify-content: center;
    height: 700px;
    width: fit-content;
    overflow: hidden;
    border-radius: 15px;
    border: 1px solid white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.video-container video {
    height: 100%;
    width: auto;
    object-fit: cover;
}

.footer-section {
    background-color: #000;
    color: white;
    padding: 4rem 2rem;
    margin-top: 2rem;
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

.video-section>p {
    font-size: 2.5rem;
    padding-bottom: 50px;
    font-family: "Cormorant Garamond", serif;
    font-weight: bolder;
}

.main-feature {
    text-align: center;
    padding: 2rem;
}

.heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 2rem;
    margin-top: 150px;
}

.heading h2 {
    font-size: 2.5rem;
    font-weight: bold;
    overflow: hidden; /* Ensures text stays within the bounds */
    white-space: nowrap; /* Prevents text from wrapping */
    border-right: 3px solid black; /* Creates a blinking cursor */
    animation: typing 3s steps(500, end), blink-caret 0.75s step-end infinite;
}


@keyframes typing {
    from { width: 0; }
    to { width: 100%; }
}

@keyframes blink-caret {
    50% { border-color: transparent; }
}

.destination-cards {
    display: flex;
    gap: 1.5rem;
    justify-content: center;
    background-color: black;
}

.card {
    width: 450px; /* Keep width the same */
    max-height: 550px; /* Reduced card height */
    border-radius: 20px;
    overflow: hidden;
    text-align: left;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
    background-color: transparent; /* Remove background color */

}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.2);
}

.card img {
    width: 100%;
    height: 90%; /* Reduced image height */
    /* object-fit: cover; */
}

.card p {
    margin-left: 10px;
    font-size: 1.25rem;
    font-weight: bold;
    color: #333;
    padding: 0.5rem 0; /* Padding for text */
    height: 10%; /* Ensures text occupies the remaining space */
}

</style>