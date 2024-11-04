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
              <label for="email" class="form-label">Email address</label>
              <input type="email" class="form-control" id="email" v-model="email"
                placeholder="Enter your email" required>
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input type="password" class="form-control" id="password" v-model="password"
                placeholder="Enter your password" required>
            </div>
  
            <p v-if="errMsg" class="text-danger">{{ errMsg }}</p>
  
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
            <p>Don't have an account? <router-link to="/sign-up" class="link-primary">Sign Up</router-link></p>
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
  
  <script setup>
  import { ref } from 'vue';
  import { getAuth, signInWithEmailAndPassword, signInWithPopup, GoogleAuthProvider, FacebookAuthProvider } from 'firebase/auth';
  import { useRouter } from 'vue-router';
  
  const email = ref('');
  const password = ref('');
  const errMsg = ref(''); // ERROR MESSAGE
  const router = useRouter(); // get a reference to our vue router
  
  const handleSubmit = async () => {
      const auth = getAuth();
      errMsg.value = ''; // Reset error message
  
      try {
          await signInWithEmailAndPassword(auth, email.value, password.value); // Firebase sign-in logic
          console.log('Successfully logged in!');
          router.push('/mainpage'); // redirect to the about page
      } catch (error) {
          switch (error.code) {
              case 'auth/invalid-email':
                  errMsg.value = 'Invalid email';
                  break;
              case 'auth/user-not-found':
                  errMsg.value = 'No account with that email was found';
                  break;
              case 'auth/wrong-password':
                  errMsg.value = 'Incorrect password';
                  break;
              default:
                  errMsg.value = 'Email or password was incorrect';
                  break;
          }
      }
  };
  
  const signInWithGoogle = async () => {
      const auth = getAuth();
      const googleProvider = new GoogleAuthProvider();
  
      try {
          const result = await signInWithPopup(auth, googleProvider);
          const user = result.user;
  
          console.log('User signed in with Google:', user);
              // Store user data in session storage
          sessionStorage.setItem('username', user.displayName || 'User');
          sessionStorage.setItem('email', user.email);
          
          router.push('/mainpage'); // Redirect to about after successful sign-in
      } catch (error) {
          console.error('Error signing in with Google:', error.code, error.message);
      }
  };
  
  const signInWithFacebook = async () => {
      const auth = getAuth();
      const facebookProvider = new FacebookAuthProvider();
  
      try {
          const result = await signInWithPopup(auth, facebookProvider);
          const user = result.user;
  
          console.log('User signed in with Facebook:', user);
          router.push('/'); // Redirect to about after successful sign-in
      } catch (error) {
          console.error('Error signing in with Facebook:', error.code, error.message);
      }
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
      padding-bottom: 110px;
  }
  
  h2 {
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
