<!-- frontend/src/views/ToastTest.vue -->

<template>
    <div class="toast-test-container">
      <h1>Toast Notification Test</h1>
      <div class="buttons">
        <button @click="showToast('add')">Show Success Toast</button>
        <button @click="showToast('remove')">Show Error Toast</button>
        <button @click="showToast('info')">Show Info Toast</button>
      </div>
  
      <ToastNotification
        v-if="isToastVisible"
        :show="isToastVisible"
        :message="toastMessage"
        :type="toastType"
        :duration="toastDuration"
        @update:show="isToastVisible = $event"
      />
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import ToastNotification from '@/components/ToastNotification.vue';
  
  export default {
    name: 'ToastTest',
    components: { ToastNotification },
    setup() {
      const isToastVisible = ref(false);
      const toastMessage = ref('');
      const toastType = ref('add');
      const toastDuration = ref(3000); // 3 seconds for testing
  
      const showToast = (type) => {
        toastType.value = type;
        switch (type) {
          case 'add':
            toastMessage.value = 'This is a success toast notification!';
            break;
          case 'remove':
            toastMessage.value = 'This is an error toast notification!';
            break;
          case 'info':
            toastMessage.value = 'This is an info toast notification!';
            break;
          default:
            toastMessage.value = 'This is a toast notification!';
        }
        isToastVisible.value = true;
      };
  
      return {
        isToastVisible,
        toastMessage,
        toastType,
        toastDuration,
        showToast,
      };
    },
  };
  </script>
  
  <style scoped>
  .toast-test-container {
    padding: 20px;
    text-align: center;
  }
  
  .buttons {
    margin: 20px 0;
  }
  
  button {
    margin: 0 10px;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
  }
  </style>
  