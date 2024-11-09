<template>
    <div class="main-container-1">
        <div class="title">
            <link href="https://fonts.googleapis.com/css2?family=Lobster+Two:wght@400;700&display=swap"
                rel="stylesheet">
            <!-- Bootstrap CSS -->
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"
                integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
                crossorigin="anonymous">


            <h1 id="#brand">wander.</h1>
        </div>
        <div ref="threeContainer" class="three-container">

            <!-- Buttons for scrolling -->
            <div class="scroll-buttons">
                <button class="explore-button" @click="scrollToExplore">
                    <div class="explore-button-text">
                        <p>Explore Wander now</p>
                    </div>
                </button>
                <button class="signup-button" @click="scrollToSignUp">
                    <div class="signup-button-text">
                        <p>Skip</p>
                        <div style="margin-left: 20px;" id="chevron-arrow-down" class="chevron">
                        </div>
                        <div style="margin-left: 20px;" id="chevron-arrow-down" class="chevron">
                        </div>
                    </div>
                </button>
            </div>

        </div>

        <div ref="exploreSection" class="container">
            <div class="left-text">
                <p>Welcome to</p>
                <p style="font-family: Lobster Two; font-size: larger; color: #3f94a7;">wander :</p>
                <p>Explore the world</p>
                <p>like</p>
                <p>never before</p>
            </div>
            <div class="right-text">
                <p>Embark on a journey of discovery with Wander, your go-to travel companion. Uncover hidden gems from
                    TikTok videos and craft the perfect itineraries that transform your <span>travel dreams into
                        reality</span> effortlessly.</p>
            </div>
        </div>

        <div class="wander-container">
            <h1>
                Here's How To: Wander With
                <span class="typed-text">{{ typeValue }}</span>
                <span class="blinking-cursor">|</span>
                <span class="cursor" :class="{ typing: typeStatus }">&nbsp;</span>
            </h1>
        </div>


        <div class="project-container">
            <div class="image-section">
                <video src="../assets/link.mp4" loop autoplay muted></video>
            </div>
            <div class="text-section">
                <p class="project-number">01</p>
                <h2 class="project-title">
                    Copy the link of the travel Tiktok of your choice!
                </h2>
            </div>
        </div>

        <hr class="divider">

        <div class="project-container">
            <div class="text-section-2">
                <p class="project-number">02</p>
                <h2 class="project-title">
                    Paste the link in our search bar and press 'Search!'
                </h2>
            </div>
            <div class="image-section">
                <video src="../assets/search.mp4" loop autoplay muted></video>
            </div>
        </div>

        <hr class="divider">

        <div class="project-container">
            <div class="image-section">
                <video src="../assets/extract.mp4" loop autoplay muted></video>
            </div>
            <div class="text-section">
                <p class="project-number">03</p>
                <h2 class="project-title">
                    View the extracted locations right away!
                </h2>
            </div>
        </div>
    </div>


    <div class="main-container-2">


        <div id="smooth-wrapper">
            <div id="smooth-content">
                <div class="transition-image"><img src="../assets/head.png"></div>
                <div class="grid-section">
                    <div class="grid-layout">
                        <div class="column column-1" data-speed="1">
                            <div class="column-content">
                                <div class="grid-image">
                                    <img src="../assets/about-scroll/scroll-1.jpeg" alt="">
                                </div>
                                <div class="grid-image">
                                    <img src="../assets/about-scroll/scroll-2.jpeg" alt="">
                                </div>
                                <div class="grid-image">
                                    <img src="../assets/about-scroll/scroll-3.jpeg" alt="">
                                </div>
                            </div>
                        </div>
                        <div class="column column-2" data-speed="1.01">
                            <div class="column-content">
                                <div class="grid-image">
                                    <img src="../assets/about-scroll/scroll-4.jpeg" alt="">
                                </div>
                                <div class="grid-image">
                                    <img src="../assets/about-scroll/scroll-5.jpeg" alt="">
                                </div>
                                <div class="grid-image">
                                    <img src="../assets/about-scroll/scroll-6.jpeg" alt="">
                                </div>
                            </div>
                        </div>
                        <div class="column column-3" data-speed="1.1">
                            <div class="column-content">
                                <div class="grid-image">
                                    <img src="../assets/about-scroll/scroll-7.jpeg" alt="">
                                </div>
                                <div class="grid-image">
                                    <img src="../assets/about-scroll/scroll-8.jpeg" alt="">
                                </div>
                                <div class="grid-image">
                                    <img src="../assets/about-scroll/scroll-9.jpeg" alt="">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="spacer"></div>

                <section class="parallax-section">
                    <img class="parallax-image" src="../assets/about-scroll/image.jpeg" data-speed="auto">
                </section>

                <div class="spacer"></div>

                <div class="pin-section">
                    <div class="pin-content pin-content-1">
                        <div class="pin-box">
                            <img class="pin-image" src="../assets/about-scroll/hori-1.jpeg">
                        </div>
                        <div class="pin-box">
                            <img class="pin-image" src="../assets/about-scroll/hori-2.jpeg">
                        </div>
                        <div class="pin-box">
                            <img class="pin-image" src="../assets/about-scroll/hori-3.jpeg">
                        </div>
                    </div>

                    <div class="pin-content pin-content-2">
                        <div class="pin-box">
                            <img class="pin-image" src="../assets/about-scroll/hori-4.jpeg">
                        </div>
                        <div class="pin-box">
                            <img class="pin-image" src="../assets/about-scroll/hori-5.jpeg">
                        </div>
                        <div class="pin-box">
                            <img class="pin-image" src="../assets/about-scroll/hori-6.jpeg">
                        </div>
                    </div>
                </div>
            </div>


            <div class="section-container">
                <div class="headline">
                    <h1>
                        Ignite your sense of<br> <span class="highlight">adventure</span> and <span
                            class="highlight-different">experience</span><br> life in ways you never thought possible!
                    </h1>
                </div>
                <div class="divider"></div>
                <div class="subheading">
                    <div class="circles">
                        <div class="circle">
                            <img src="../assets/about-scroll/scroll-3.jpeg" alt="Ocean thumbnail 1" />
                        </div>
                        <div class="circle">
                            <img src="../assets/about-scroll/scroll-5.jpeg" alt="Ocean thumbnail 2" />
                        </div>
                        <div class="circle">
                            <img src="../assets/about-scroll/scroll-7.jpeg" alt="Ocean thumbnail 3" />
                        </div>
                    </div>
                    <h2 class="subheading-text">choose wander.</h2>
                </div>
            </div>
        </div>




        <div class="carousel-section" ref="carouselSection">
            <div class="carousel-header">
                <h2>Your next destination...</h2>
            </div>
            <div class="carousel-container">
                <div class="carousel-track" ref="carouselTrack">
                    <!-- Double the images for seamless loop -->
                    <div v-for="(image, index) in [...images, ...images, ...images, ...images, ...images]" :key="index"
                        class="carousel-slide">
                        <div class="image-container">
                            <img :src="image.src" :alt="image.alt || `Slide ${index + 1}`">
                            <div class="image-caption">{{ image.country }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>


        <div class="call-to-action">
            <h3>What are you waiting for? Start <span>Wander</span>ing.</h3><br>
        </div>

        <div ref="signUpSection" class="auth-buttons">
            <button @click="navigateTologin" class="login-btn">Log in</button>
            <button @click="navigateTosignup" class="signup-btn">Sign up</button>
        </div>


    </div>

</template>


<script>
import { onMounted, ref } from 'vue';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { ColorManagement } from 'three';
import { nextTick } from 'vue';

// Enable color management
ColorManagement.enabled = true;

gsap.registerPlugin(ScrollTrigger);


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

            typeValue: "",
            typeStatus: false,
            displayTextArray: ["Friends", "Family", "Purpose", "Curiosity", "Excitement"],
            typingSpeed: 100,
            erasingSpeed: 100,
            newTextDelay: 800,
            displayTextArrayIndex: 0,
            charIndex: 0,

        };
    },
    props: {},
    created() {
        setTimeout(this.typeText, this.newTextDelay + 200);
    },
    setup() {
        ScrollTrigger.refresh()
        const threeContainer = ref(null);
        const carouselSection = ref(null);
        const carouselTrack = ref(null);
        let globe = null;
        let renderer = null;
        // const exploreSection = ref(null);
        // const signUpSection = ref(null);

        const camera = new THREE.PerspectiveCamera(
            75,
            window.innerWidth / window.innerHeight,
            0.1,
            1000
        );
        camera.position.z = 5;


        const handleResize = () => {
            if (threeContainer.value && renderer) {
                const width = threeContainer.value.clientWidth;
                const height = threeContainer.value.clientHeight;

                // Update camera
                camera.aspect = width / height;
                camera.updateProjectionMatrix();

                // Update renderer
                renderer.setSize(width, height);
            }
        }


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
                    // if (entry.target === carouselSection.value) {
                    //     carouselSection.value.style.opacity = entry.intersectionRatio;
                    // }
                });
            }, options);

            observer.observe(threeContainer.value);
            // observer.observe(carouselSection.value);
        };

        onMounted(() => {


            window.addEventListener('resize', handleResize);
            // Call handleResize once to ensure everything is properly sized initially
            handleResize();

            window.addEventListener('load', () => {
                document.body.offsetHeight; // Force a reflow/repaint
                ScrollTrigger.refresh();// Recalculate trigger positions
            });
            let gridTl = gsap.timeline({
                scrollTrigger: {
                    trigger: ".transition-image",
                    scrub: 1,
                    start: "bottom top",
                    endTrigger: ".grid-section",
                    end: "bottom center",
                    markers: false,
                    // pin: true,
                },
                defaults: {
                    ease: "power1.inOut"
                }
            });

            nextTick(() => {
                if (document.querySelector(".grid-section")) {
                    gridTl.add("start")
                        .from(".grid-layout", {
                            ease: "power1",
                            scale: 3
                        }, "start")
                        .from(".column-1 .grid-image", {
                            duration: 0.4,
                            xPercent: i => -((i + 1) * 40 + i * 100),
                            yPercent: i => (i + 1) * 40 + i * 100
                        }, "start")
                        .from(".column-3 .grid-image", {
                            duration: 0.4,
                            xPercent: i => (i + 1) * 40 + i * 100,
                            yPercent: i => (i + 1) * 40 + i * 100
                        }, "start");
                }
            })

            // Parallax effect for the parallax section
            gsap.from(".parallax-section", {
                scale: 1 / 3,
                scrollTrigger: {
                    trigger: ".parallax-section",
                    scrub: 1
                }
            });

            // Pinning and horizontal scroll animation for the pin section
            let pinSection = document.querySelector(".pin-section");
            let pinContent1 = document.querySelector(".pin-content-1");
            let pinContent2 = document.querySelector(".pin-content-2");

            let pinTl = gsap.timeline({
                scrollTrigger: {
                    pin: true,
                    trigger: pinSection,
                    scrub: true,
                    start: "top top",
                    end: () => `+=${pinContent1.offsetWidth}`,
                    invalidateOnRefresh: true
                }
            });

            pinTl.fromTo(".pin-content-1", {
                x: () => document.body.clientWidth * 0.9
            }, {
                x: () => -(pinContent1.offsetWidth),
                ease: "none"
            }, 0);

            pinTl.fromTo(".pin-content-2", {
                x: () => -pinContent2.offsetWidth + document.body.clientWidth * 0.1
            }, {
                x: () => document.body.clientWidth,
                ease: "none"
            }, 0);




            if (!threeContainer.value) return;

            // Scene setup (same as before)
            const scene = new THREE.Scene();

            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.outputColorSpace = THREE.SRGBColorSpace;
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
                    // texture.encoding = THREE.sRGBEncoding;
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
                        renderer.setPixelRatio(window.devicePixelRatio); // Add this line
                        renderer.render(scene, camera);
                    }
                    animate();
                    // window.addEventListener('DOMContentLoaded', () => {
                    //     // Check if the necessary DOM elements are available
                    //     const gridSection = document.querySelector('.grid-section');
                    //     if (gridSection) {
                    //         animate();
                    //     }
                    // });
                },
                undefined,
                (error) => {
                    console.error('An error occurred loading the texture.', error);
                }
            );


        });

        return { threeContainer, carouselSection, carouselTrack, handleResize };
    },
    mounted() {

        this.startAutoScroll();
        const video = document.querySelector('video');
        video.play().catch(function (error) {
            console.log("Video autoplay failed:", error);
        });
    },

    beforeUnmount() {

        window.removeEventListener('resize', this.handleResize);

        window.removeEventListener('load', () => {
            ScrollTrigger.refresh();
        });
        this.stopAutoScroll();
    },
    methods: {
        // Scroll to Explore section
        scrollToExplore() {
            this.$refs.exploreSection.scrollIntoView({ behavior: 'smooth' });
        },
        // Scroll to Sign Up section
        scrollToSignUp() {
            this.$refs.signUpSection.scrollIntoView({ behavior: 'smooth' });
        },

        typeText() {
            if (this.charIndex < this.displayTextArray[this.displayTextArrayIndex].length) {
                if (!this.typeStatus) this.typeStatus = true;
                this.typeValue += this.displayTextArray[this.displayTextArrayIndex].charAt(
                    this.charIndex
                );
                this.charIndex += 1;
                setTimeout(this.typeText, this.typingSpeed);
            } else {
                this.typeStatus = false;
                setTimeout(this.eraseText, this.newTextDelay);
            }
        },
        eraseText() {
            if (this.charIndex > 0) {
                if (!this.typeStatus) this.typeStatus = true;
                this.typeValue = this.displayTextArray[this.displayTextArrayIndex].substring(
                    0,
                    this.charIndex - 1
                );
                this.charIndex -= 1;
                setTimeout(this.eraseText, this.erasingSpeed);
            } else {
                this.typeStatus = false;
                this.displayTextArrayIndex += 1;
                if (this.displayTextArrayIndex >= this.displayTextArray.length)
                    this.displayTextArrayIndex = 0;
                setTimeout(this.typeText, this.typingSpeed + 1000);
            }
        },


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
            // Code to navigate to login page
            this.$router.push('/log-in'); // Assuming you're using Vue Router
        },
        navigateTosignup() {
            // Code to navigate to sign up page
            this.$router.push('/sign-up'); // Assuming you're using Vue Router
        }

    },


};

</script>

<style scoped>
.scroll-buttons {
    position: absolute;
    /* Make the buttons overlay the three-container */
    bottom: 150px;
    /* Align to the bottom of the three-container */
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-between;
    /* Distribute the buttons evenly */
    align-items: center;
    /* Center buttons vertically */
    /* Adjust padding as necessary */
    z-index: 9999;
    /* Ensure the buttons are on top */
}

/* Center the Explore button directly under the globe */
.explore-button {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
}

/* Keep the Sign Up button on the far right */
.signup-button {
    margin-left: auto;
    margin-right: 20px;
    margin-bottom: 50px;
}

.explore-button-text {
    font-size: 1.5rem;
    padding: 5px;
    margin: 0;

}

.signup-button-text {
    display: flex;
    flex-direction: column;
    right: 2px;
    /* Stack items vertically */
    align-items: center;
    /* Center items horizontally */
    animation: bounce 2s 30;
    color: #a3a7ae;
    /* gap: 8px; */
    /* Add space between the chevrons and the text */
    animation: bounce 2s 30;
    color: #a3a7ae;
}

.signup-button-text p {
    font-size: 1.5rem;
    rotate: 90deg;
}

.chevron {
    border-right:
        4px solid #a3a7ae;
    border-bottom:
        4px solid #a3a7ae;
    width: 20px;
    height: 20px;
    right: 11px;
}

#chevron-arrow-down {
    transform: rotate(45deg);
}

.explore-button,
.signup-button {
    padding: 0;
    font-size: 1rem;
    color: #fff;
    background-color: rgba(0, 0, 0, 0.8);
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: transform 0.3s ease, background-color 0.3s ease, color 0.3s ease;
}


.explore-button-text p {
    width: 0;
    overflow: hidden;
    /* Ensure the text is not visible until the typewriter effect*/
    border-right: 2px solid white;
    /* The cursor*/
    font-size: 1.5rem;
    white-space: nowrap;
    /* Keeps the text on a single line */
    animation: typing 5s forwards infinite, blinking 1.5s step-end infinite;
    ;
}

@media (min-width: 375px) and (max-width: 567px) {
    .signup-button {
        margin-left: auto;
        margin-right: 20px;
        margin-top: 100px;
        top: 100px;
    }
}

/* The typing animation */
@keyframes typing {
    from {
        width: 0
    }

    to {
        width: 100%
    }
}

@keyframes blinking {

    from,
    to {
        border-right-color: transparent;
    }

    50% {
        border-right-color: white;
    }
}

.main-container-1 {
    height: auto;
    overflow-y: hidden;
    overflow-x: hidden;
    background-color: black;
    color: white;
    margin: 0;
    padding: 0;
    padding-bottom: 150px;
}

.main-container-2 {
    height: auto;
    overflow-y: hidden;
    overflow-x: hidden;
    background-color: white;
    color: black;
    margin: 0;
    padding: 0;
}

.three-container {
    position: relative;
    width: 100vw;
    height: 100vh;
    /* Increase the height to make the globe bigger */
    overflow: hidden;
    top: 0;
    z-index: 1;
}



@media (min-width: 768px) and (max-width: 921px) {
    .main-container-1 #brand {
        font-size: 95x !important;
    }
}

@media (min-width: 576px) and (max-width: 767px) {
    .main-container-1 #brand {
        font-size: 70px !important;
    }
}


@media(max-width: 575px) and (min-width: 0px) {
    .main-container-1 #brand {
        font-size: 50px !important;
    }
}

@media(max-width: 575px) and (min-width: 0px) {
    .three-container {
        width: 100vw;
        height: 70vh;
        overflow: hidden;
        top: 0;
    }
}


@media (min-width: 992px) and (max-width: 1200px) {
    .three-container {
        width: 100vw;
        height: 100vh;
        /* Increase the height to make the globe bigger */
        overflow: hidden;
        top: 0;
    }
}


@media (min-width: 992px) and (max-width: 1199px) {
    .three-container {
        width: 100vw;
        height: 100vh;
        /* Increase the height to make the globe bigger */
        overflow: hidden;
        top: 0;
    }
}

@media (max-width:576px) {
    .three-container {
        width: 100vw;
        height: 70vh;
        overflow: hidden;
        top: 0;
        margin-bottom: 150px;
    }

    .scroll-buttons {
        position: absolute;
        /* Make the buttons overlay the three-container */
        bottom: -5px;
        /* Align to the bottom of the three-container */
        left: 0;
        right: 0;
        display: flex;
        justify-content: space-between;
        /* Distribute the buttons evenly */
        align-items: center;
        /* Center buttons vertically */
        padding: 10px 20px;
        /* Adjust padding as necessary */
        z-index: 9999;
        /* Ensure the buttons are on top */
    }
}

@media (min-width: 1200px) {
    .three-container {
        width: 100vw;
        height: 100vh;
        /* Increase the height to make the globe bigger */
        overflow: hidden;
        top: 0;
    }
}



@media (min-width: 576px) and (max-width: 767px) {
    .three-container {
        width: 100vw;
        height: 80vh;
        overflow: visible;
    }

    .scroll-buttons {
        position: absolute;
        /* Make the buttons overlay the three-container */
        bottom: -5px;
        /* Align to the bottom of the three-container */
        left: 0;
        right: 0;
        display: flex;
        justify-content: space-between;
        /* Distribute the buttons evenly */
        align-items: center;
        /* Center buttons vertically */
        padding: 10px 20px;
        /* Adjust padding as necessary */
        z-index: 9999;
        /* Ensure the buttons are on top */
    }
}

@media (min-width: 768px) and (max-width: 921px) {

    /* Styles for screens 576px - 767px */
    .three-container {
        width: 100vw;
        height: 85vh;
        overflow: visible;
    }

    .scroll-buttons {
        position: absolute;
        /* Make the buttons overlay the three-container */
        bottom: -5px;
        /* Align to the bottom of the three-container */
        left: 0;
        right: 0;
        display: flex;
        justify-content: space-between;
        /* Distribute the buttons evenly */
        align-items: center;
        /* Center buttons vertically */
        padding: 10px 20px;
        /* Adjust padding as necessary */
        z-index: 9999;
        /* Ensure the buttons are on top */
    }
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
    padding: 20px;
    text-align: center;
    margin-top: 150px;
}

.carousel-header h2 {
    font-size: 2rem;
    margin-bottom: 20px;
    color: #3f94a7;
}

/* Carousel container styling */
.carousel-container {
    overflow: hidden;
    width: 100%;
    display: flex;
    justify-content: center;
}

.carousel-track {
    display: flex;
    animation: scroll 150s linear infinite;
    gap: 20px;
    /* Adjust space between images */
}

@keyframes scroll {
    0% {
        transform: translateX(0);
    }

    100% {
        transform: translateX(-50%);
    }

    /* Adjust depending on total width */
}

/* Image container */
.image-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

/* Responsive styles */

/* Large screens (desktop) */
@media (min-width: 1024px) {
    .carousel-header h2 {
        font-size: 2.5rem;
    }

    .carousel-slide {
        flex: 1 1 220px;
    }

    .image-container img {
        width: 220px;
        height: 350px;
        object-fit: cover;
        border-radius: 15px;
    }

    .image-caption {
        font-size: 1rem;
        margin-top: 8px;
        color: #3f94a7;
    }
}

/* Medium screens (tablet) */
@media (min-width: 768px) and (max-width: 1023px) {
    .carousel-header h2 {
        font-size: 2rem;
    }

    .carousel-slide {
        flex: 1 1 180px;
    }

    .image-container img {
        width: 180px;
        height: 300px;
        object-fit: cover;
        border-radius: 12px;
    }

    .image-caption {
        font-size: 0.9rem;
        margin-top: 6px;
        color: #3f94a7;
    }
}

/* Small screens (mobile) */
@media (max-width: 767px) {
    .carousel-header h2 {
        font-size: 1.5rem;
    }

    .carousel-slide {
        flex: 1 1 150px;
    }

    .image-container img {
        width: 150px;
        height: 250px;
        object-fit: cover;
        border-radius: 10px;
    }

    .image-caption {
        font-size: 0.8rem;
        margin-top: 4px;
        color: #3f94a7;
    }
}




.text-container {
    color: #000000;
    width: 40%;
    display: flex;
    flex-direction: column;
    gap: 10px;
    text-align: left;
    margin-left: 90px;
}

.project-title {
    text-align: left;
    font-size: 30px;
}

.view-project {
    background-color: #000000;
    color: #ffffff;
    width: fit-content;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    padding: 10px 20px;
    margin-top: 10px;
    margin-left: 0px;
}


.transition-image {
    width: 100vw;
    /* Set width to 100% of the container */
    max-width: 100vw;
    /* Restrict it to the viewport width */
    height: auto;
    /* Maintain aspect ratio */
    margin-bottom: 150px;
    object-fit: contain;
    display: flex;
    justify-content: center;
}

.transition-image img {
    width: 100%;
    height: auto;
    object-fit: contain;
}

@media (min-width:375px) and (max-width: 575px) {
    .container {
        flex-direction: column;
        width: 100vw;
        margin-bottom: 60px;
        background-color: #000000;
        color: white;
        display: flex;
        align-items: center;
        height: 100vh;
        padding: 0 20px;
    }

    .left-text {
        font-size: 5.5vw;
        flex: 3;
        margin-top: 100px;
        margin-bottom: 90px;
    }

    .right-text {
        font-size: 3vw;
        margin-bottom: 100px;
        padding-bottom: 100px;
        padding-left: 30px;
        padding-right: 30px;
    }
}

@media (min-width: 767px) and (max-width: 991px) {

    /* Styles for screens 576px - 767px */
    .container {
        width: 100vw;
        flex-direction: column;
        background-color: #000000;
        color: white;
        display: flex;
        align-items: center;
        height: 100vh;
        padding: 100px 20px;
        margin-bottom: 100px;
        gap: 100px;
        flex: 5;

    }

    .left-text {
        font-size: 5vw;
        flex: 3;
        margin-top: 100px;
    }

    .right-text {
        font-size: 3vw;
        margin-bottom: 100px;
        padding-bottom: 100px;
    }
}

@media (min-width: 576px) and (max-width: 766px) {
    .container {
        flex-direction: column;
        width: 100vw;
        margin-bottom: 100px;
        background-color: #000000;
        color: white;
        display: flex;
        align-items: center;
        height: 100vh;
        padding: 0 20px;
    }

    .left-text {
        font-size: 8vw;
        flex: 3;
        margin-bottom: 60px;
        padding-top: 0px;
        line-height: 1;
    }

    .right-text {
        font-size: 3vw;
        padding-bottom: 100px;
        padding-left: 20px;
        padding-right: 20px;
        margin-bottom: 100px;

        /* Adjust right text size for small screens */
    }
}

@media (min-width: 992px) {
    .left-text {
        flex: 1;
        font-size: 4vw;
        font-weight: bold;
        line-height: 1.2;
        padding: 30px;
    }

    .right-text {
        flex: 1;
        font-size: 1.5vw;
        line-height: 1.5;
        max-width: 50%;
    }

    .container {
        background-color: #000000;
        color: white;
        display: flex;
        align-items: center;
        height: 100vh;
        padding: 0 20px;
        flex-direction: row;
    }
}

.right-text span {
    background-color: #3f94a7;
    color: #ffffff;
}


.project-container {
    display: flex;
    align-items: center;
    margin-bottom: 0;
    padding-left: 50px;
    padding-right: 50px;
}




.image-section {
    flex: 1;
    border-radius: 20px;
}

.image-section video {
    width: 100%;
    height: auto;
    border-radius: 20px;
    object-fit: contain;
}

.text-section {
    flex: 1;
    padding-left: 80px;
}

.text-section-2 {
    flex: 1;
    padding-right: 80px;
}


.divider {
    width: 100%;
    border: none;
    border-top: 1px solid white;
    margin: 30px 0;
}

.project-number {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 50px;
    color: #3f94a7;
}

.project-number-2 {
    font-size: 1rem;
}

@media (min-width: 375px) and (max-width: 767px) {
    .project-container {
        flex-direction: column;
        padding-left: 20px;
        padding-right: 20px;
    }

    .text-section {
        padding-left: 0;
        padding-top: 20px;
    }

    .image-section {
        width: 100%;
        margin-top: 20px;
    }

    .image-section video {
        width: 100%;
        height: auto;
    }

    .project-number {
        font-size: 1.5rem;
        margin-bottom: 30px;
    }

    .project-title {
        font-size: 1.5rem;
    }
}


@media(max-width:575px) {
    .wander-container h1 {
        font-size: 2rem;
        line-height: 1;
        line-wrap: wrap;
        text-align: center;

        span.typed-text {
            color: #3f94a7;
        }
    }

    .blinking-cursor {
        font-size: 2rem;
        animation: 1s blink step-end infinite;
    }
}

@media (min-width: 576px) and (max-width: 766px) {
    .wander-container h1 {
        margin-top: 1px;
        font-size: 1.8rem;
        line-height: 1;

        span.typed-text {
            color: #3f94a7;
        }
    }

    .blinking-cursor {
        font-size: 2.5rem;
        animation: 1s blink step-end infinite;
    }
}

@media (min-width: 767px) and (max-width: 991px) {
    .wander-container h1 {
        font-size: 2.5rem;
        line-height: 1;

        span.typed-text {
            color: #3f94a7;
        }
    }

    .blinking-cursor {
        font-size: 3rem;
        animation: 1s blink step-end infinite;
    }

    .wander-container {
        margin-top: 450px;
    }
}

@media (min-width: 992px) {
    h1 {
        font-size: 3.5rem;
        font-weight: normal;

        span.typed-text {
            color: #3f94a7;
        }
    }

    .blinking-cursor {
        font-size: 6rem;
        color: #2c3e50;
        animation: 1s blink step-end infinite;
    }
}


.wander-container {
    width: 100%;
    height: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 50px;
}



@keyframes blink {

    from,
    to {
        color: transparent;
    }

    50% {
        color: #2c3e50;
    }
}






* {
    position: relative;
    box-sizing: border-box;
}

.smooth-content {
    padding-top: 1000px;
}


.parallax-section {
    height: 100vh;
    width: 100%;
    overflow: hidden;
    top: 0;
    padding: 0 1rem;
    transform-origin: center top;
}

.parallax-image {
    height: 200vh;
    width: 100%;
    object-fit: cover;
    will-change: transform;
}


.grid-section {
    overflow: visible;
    /* z-index: 2; */
    min-height: 100vh;
}

.grid-layout {
    display: flex;
    display: grid;
    height: 100%;
    width: 100%;
    grid-template-columns: 1fr 1fr 1fr;
    grid-gap: 1rem;
    transform-origin: center top;
}

.column {
    height: 100%;
}

.panel {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.column-content {
    display: grid;
    grid-template-rows: 45vh 45vh 45vh;
    grid-gap: 1rem;
    height: 100%;
}

.grid-image {
    width: 100%;
    position: relative;
}

.grid-image img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.pin-section {
    height: 100vh;
    overflow: hidden;
    display: grid;
    grid-row-gap: 1rem;
    grid-template-rows: 1fr 1fr;
}

.pin-content {
    width: 300%;
    display: grid;
    grid-column-gap: 1rem;
    grid-template-columns: 1fr 1fr 1fr;
    will-change: transform;
}

.pin-box {
    height: 100%;
    width: 100%;
}

.pin-image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.spacer {
    height: 20vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.scroll-letter {
    fill: #fff;
}

.smoother-letter,
#mouse-wheel {
    fill: #88ce02;
}

.by-greensock-letter {
    fill: #fff;
    opacity: 0.6;
}

#mouse-outline {
    fill: none;
    stroke: #fff;
    stroke-miterlimit: 10;
    stroke-width: 13px;
}





.section-container {
    margin-top: 10px;
    text-align: left;
    padding: 2rem;
    font-family: Arial, sans-serif;
}


.headline h1 {
    font-size: 2.5rem;
    font-weight: bold;
    line-height: 1.4;
    margin-bottom: 1rem;
}

.highlight {
    font-weight: 600;
    font-style: italic;
    color: #3f94a7;
}

.highlight-different {
    font-weight: 600;
    background-color: #3f94a7;
    color: white;
    display: inline-block;
    padding-bottom: 0.2rem;
}

.divider {
    border-bottom: 2px solid black;
    margin: 60px 0px;
}

.subheading {
    display: flex;
    justify-content: right;
    color: #3f94a7;
}

.circles {
    display: flex;
    gap: 1rem;
    align-items: center;
    margin-right: 1.2rem;
}

.circle {
    width: 55px;
    height: 55px;
    border-radius: 50%;
    overflow: hidden;
    flex-shrink: 0;
}

.circle img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.subheading-text {
    font-size: 5rem;
    font-weight: bold;
    margin: 0;
}

@media (min-width: 768px) and (max-width: 991px) {
    .subheading {
        justify-content: flex-end;
    }

    .circle {
        width: 35px;
        height: 35px;
    }

    .subheading-text {
        font-size: 3rem;
    }
}


@media (min-width: 576px) and (max-width: 767px) {
    .circle {
        width: 30px;
        height: 30px;
    }

    .subheading-text {
        font-size: 2.5rem;
        font-weight: bolder;
    }
}

@media (min-width: 375px) and (max-width: 575px) {
    .circle {
        width: 25px;
        height: 25px;
        justify-content: right;
    }

    .subheading-text {
        font-size: 2.5rem;
        font-weight: bolder;
        margin-left: 0;
    }

    .subheading {
        text-align: right;
        display: flex;
        align-items: center;
    }

    .circles {
        justify-content: right;
        display: flex;
        margin-right: 0;
    }
}






.auth-buttons {
    display: flex;
    gap: 16px;
    align-items: center;
    justify-content: center;
    margin-top: 50px;
    margin-bottom: 150px;
}

.login-btn,
.signup-btn {
    padding: 10px 24px;
    font-size: 15px;
    font-weight: 500;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 1px solid #3f94a7;
    color: #3f94a7;
    background-color: #ffffff;
}

.login-btn:hover {
    background-color: #bdd7ff;
    border-color: #d1d5db;
}

.signup-btn {
    background-color: #3f94a7;
    border: 1px solid #3f94a7;
    color: white;
}

.signup-btn:hover {
    background-color: #378597;
    border-color: #378597;
}

/* Optional: Add focus states for accessibility */
.login-btn:focus,
.signup-btn:focus {
    outline: 2px solid #378597;
    outline-offset: 2px;
}

/* Optional: Add active states */
.login-btn:active {
    background-color: #e5e7eb;
}

.signup-btn:active {
    background-color: #3f94a7;
}

/* Optional: Add responsive design */
@media (max-width: 640px) {

    .login-btn,
    .signup-btn {
        padding: 8px 20px;
        font-size: 14px;
    }
}


.call-to-action {
    margin-top: 100px;
    font-weight: 200px;
    text-align: center;
}

.call-to-action h3 {
    font-size: 35px;
    animation: bounce 1s infinite;
}

@keyframes bounce {

    0%,
    100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-10px);
    }
}

.call-to-action span {
    color: #3f94a7;
    /* font-style: italic; */
}
</style>