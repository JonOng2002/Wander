<template>
  <div class="register-container">
    <h1>Create an Account</h1>
    
    <p><input type="text" placeholder="Name" v-model="name" /></p>
    <p><input type="text" placeholder="Email" v-model="email" /></p>
    <p><input type="password" placeholder="Password" v-model="password" /></p>
    <p><button @click="register">Submit</button></p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { getAuth, createUserWithEmailAndPassword, updateProfile } from 'firebase/auth';
import { useRouter } from 'vue-router';

const name = ref('');
const email = ref('');
const password = ref('');
const router = useRouter();

const register = () => {
  const auth = getAuth();
  
  createUserWithEmailAndPassword(auth, email.value, password.value)
    .then((userCredential) => {
      // User registered successfully
      const user = userCredential.user;
      
      // Now update the user profile with the display name
      updateProfile(user, {
        displayName: name.value,
      })
      .then(() => {
        console.log('Successfully updated profile with name!');
        router.push('/feed'); // Redirect to feed after successful registration
      })
      .catch((error) => {
        console.error('Error updating profile:', error);
      });
    })
    .catch((error) => {
      console.error('Error during registration:', error.code);
      alert(error.message);
    });
};
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  text-align: center;
}

input {
  display: block;
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
  border: 1px solid #ccc;
}

button {
  padding: 10px 20px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>