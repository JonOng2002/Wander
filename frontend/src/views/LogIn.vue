<template>
    <div class="container-fluid d-flex align-items-center justify-content-center min-vh-100 p-0">
        <div class="row w-100 g-0 align-items-center">
            <!-- Left Side - Form Section -->
            <div class="col-md-6 px-5">
                <div class="mb-4">
                    <h1 class="display-4">wander.</h1>
                    <h2>Welcome Back!</h2>
                    <p>Enter your Credentials to access your account</p>
                </div>

                <form @submit.prevent="handleSubmit" class="signup-form">
                    <div class="mb-3">
                        <label for="name" class="form-label">Name</label>
                        <input type="text" class="form-control" id="name" v-model="form.name"
                            placeholder="Enter your name" required>
                    </div>

                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" v-model="form.password"
                            placeholder="Enter your password" required>
                    </div>

                    <div class="form-check mb-4">
                        <input class="form-check-input" type="checkbox" id="terms" v-model="form.agreeToTerms">
                        <label class="form-check-label" for="terms">
                            Remember for 30 days
                        </label>
                    </div>

                    <button id="signupBtn" type="submit" class="btn w-100 mb-3">Log In</button>
                </form>

                <div class="text-center mb-3">
                    <p>Or</p>
                </div>

                <div class="d-flex justify-content-between">
                    <button id="google" class="btn btn-outline-primary flex-fill me-2" @click="signInWithGoogle">
                        Sign in with Google <img src="../assets/google.png" alt="Google" class="me-2"
                            style="width: 20px;">
                    </button>
                    <button id="facebook" class="btn btn-outline-dark flex-fill" @click="signInWithFacebook">
                        Sign in with Facebook <img src="../assets/facebook.png" alt="Facebook" class="me-2"
                            style="width: 20px;">
                    </button>
                </div>

                <div class="text-center mt-4">
                    <p>Don't have an account? <router-link to="/sign-in" class="link-primary">Sign Up</router-link></p>
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
import { auth, googleProvider, facebookProvider } from "@/firebase";
import { signInWithPopup } from 'firebase/auth';  // Ensure this import is correct

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
        async signInWithGoogle() {
            try {
                const result = await signInWithPopup(auth, googleProvider);  // Make sure this is called correctly
                const user = result.user;  // User info
                console.log('User signed in:', user);

                // Redirect on successful sign-in
                this.$router.push('/');
            } catch (error) {
                console.error('Error signing in with Google:', error.code, error.message);
                alert('Failed to sign in. Please try again.');
            }
        },
        async signInWithFacebook() {
            try {
                const result = await signInWithPopup(auth, facebookProvider);
                const user = result.user;  // User information
                console.log('User signed in with Facebook:', user);

                // Redirect or perform any post-login action here
                this.$router.push('/');
            } catch (error) {
                console.error('Error signing in with Facebook:', error.code, error.message);
                alert('Failed to sign in with Facebook. Please try again.');
            }
        },
        handleSubmit() {
            if (!this.form.agreeToTerms) {
                alert('Please agree to the terms and policy');
                return;
            }
            if (!this.form.name || !this.form.email || !this.form.password) {
                alert('Please fill in all fields: Name, Email, and Password.');
                return;
            }
            // Handle form submission logic (e.g., sending data to an API)
            console.log('Sign up data:', this.form);
            this.$router.push('/');  // Redirect after form submission (modify route if necessary)
        },
    },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Lobster+Two:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;700&family=Roboto:wght@400;700&display=swap');


body {
    font-family: 'Lobster Two', cursive;
    overflow: hidden;
}

h1 {
    font-family: 'Lobster Two', cursive;
    padding-bottom: 110px;
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
    background-color: #6c757d;
    /* Bootstrap gray */
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
.container-fluid,
.row {
    padding: 0;
    margin: 0;
}
</style>
