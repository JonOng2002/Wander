<template>
    <div class="container-fluid d-flex align-items-center justify-content-center min-vh-100 p-0">
        <div class="row w-100 g-0 align-items-center">
            <!-- Left Side - Form Section -->
            <div class="col-md-6 px-5">
                <div class="mb-4">
                    <h1 class="display-4">wander.</h1>
                    <h2>Get Started Now</h2>
                </div>

                <form @submit.prevent="handleSubmit" class="signup-form">
                    <div class="mb-3">
                        <label for="name" class="form-label">Name</label>
                        <input type="text" class="form-control" id="name" v-model="form.name"
                            placeholder="Enter your name" required>
                    </div>
                    <div class="mb-3">
                        <label for="email" class="form-label">Email address</label>
                        <input type="email" class="form-control" id="email" v-model="form.email"
                            placeholder="Enter your email" required>
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" v-model="form.password"
                            placeholder="Enter your password" required>
                    </div>

                    <div class="form-check mb-4">
                        <input class="form-check-input" type="checkbox" id="terms" v-model="form.agreeToTerms">
                        <label class="form-check-label" for="terms">
                            I agree to the <a href="#" class="link-primary">terms & policy</a>
                        </label>
                    </div>

                    <button id="signupBtn" type="submit" class="btn w-100 mb-3">Sign Up</button>
                </form>

                <div class="text-center mb-3">
                    <p>Or</p>
                </div>

                <div class="d-flex justify-content-between">
                    <button id="google" class="btn btn-outline-primary flex-fill me-2" @click="signInWithGoogle">
                        Sign in with Google <img src="../assets/google.png" alt="Google" class="me-2" style="width: 20px;">
                    </button>
                    <button id="facebook" class="btn btn-outline-dark flex-fill" @click="signInWithFacebook">
                        Sign in with Facebook <img src="../assets/facebook.png" alt="Facebook" class="me-2"
                            style="width: 20px;">
                    </button>
                </div>

                <div class="text-center mt-4">
                    <p>Have an account? <router-link to="/log-in" class="link-primary">Sign in</router-link></p>
                </div>
            </div>

            <!-- Right Side - Image Section -->
            <div class="col-md-6 d-none d-md-block p-0">
                <img src="../assets/boat.jpg" class="img-fluid vh-100 w-100" style="object-fit: cover;"
                    alt="Boat with Mountains in the background">
            </div>
        </div>
    </div>
</template>

<script>
import { auth, googleProvider, facebookProvider, db } from "@/firebase";
import { signInWithPopup } from "firebase/auth";
import { doc, setDoc } from "firebase/firestore"; // Import Firestore methods

export default {
    data() {
        return {
            form: {
                name: '',
                email: '',
                password: '',
                agreeToTerms: false,
            },
        };
    },
    methods: {
        // Store user data in Firestore
        async storeUserData(userId, name, email) {
            try {
                const userRef = doc(db, "users", userId);
                await setDoc(userRef, {
                    name: name,
                    email: email,
                    savedPlaces: [],
                    generatedItineraries: []
                }, { merge: true }); // Merge to avoid overwriting existing fields
                console.log('User data saved in Firestore');
            } catch (error) {
                console.error('Error storing user data:', error);
            }
        },

        async signInWithGoogle() {
            try {
                const result = await signInWithPopup(auth, googleProvider);
                const user = result.user;

                // Save user data in Firestore
                await this.storeUserData(user.uid, user.displayName, user.email);

                // Redirect after successful sign-in
                this.$router.push('/');
            } catch (error) {
                console.error('Error signing in with Google:', error.code, error.message);
            }
        },

        async signInWithFacebook() {
            try {
                const result = await signInWithPopup(auth, facebookProvider);
                const user = result.user;

                // Save user data in Firestore
                await this.storeUserData(user.uid, user.displayName, user.email);

                // Redirect after successful sign-in
                this.$router.push('/');
            } catch (error) {
                console.error('Error signing in with Facebook:', error.code, error.message);
            }
        },

        async handleSubmit() {
            if (!this.form.agreeToTerms) {
                alert('Please agree to the terms and policy');
                return;
            }
            if (!this.form.name || !this.form.email || !this.form.password) {
                alert('Please fill in all fields: Name, Email, and Password.');
                return;
            }

            // Assuming you'd later implement Firebase Email/Password auth
            try {
                const user = await auth.createUserWithEmailAndPassword(this.form.email, this.form.password);
                
                // Store user data in Firestore
                await this.storeUserData(user.uid, this.form.name, this.form.email);

                // Redirect after form submission
                this.$router.push('/');
            } catch (error) {
                console.error('Error signing up with email:', error.code, error.message);
            }
        }
    },
};

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Lobster+Two:wght@400;700&display=swap');

body {
    font-family: 'Lobster Two', cursive;
    overflow: hidden;
}

h1 {
    font-family: 'Lobster Two', cursive;
    padding-bottom: 60px;
}

h2 {
    font-family: 'Cormorant Garamond';
    font-weight: bolder;
}

.container-fluid {
    min-height: 100vh;
}

.signup-form input {
    margin-bottom: 15px;
}

.signup-form button {
    margin-bottom: 10px;
}

/* Change button hover background color to gray */
#apple:hover {
    background-color: #6c757d; /* Bootstrap gray */
    color: #fff;
}

#signupBtn {
    background-color: #3A5B22;
    color: white;
}

#signupBtn:hover {
    background-color: #4c7231;
}

.col-md-6.px-4 {
    padding-left: 0;
    padding-right: 0;
}

.g-0 {
    margin-right: 0;
    margin-left: 0;
}

/* Ensure no padding or margin on sides */
.container-fluid, .row {
    padding: 0;
    margin: 0;
}

</style>
