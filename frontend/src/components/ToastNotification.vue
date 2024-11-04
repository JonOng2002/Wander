<template>
  <div :class="['custom-toast', { active: toastActive }, toastType]">
    <div class="toast-content">
      <!-- Action Icon -->
      <i :class="['fas', toastType === 'add' ? 'fa-check' : (toastType === 'remove' ? 'fa-times' : 'fa-info-circle'), 'action-icon']"></i>

      <!-- Message -->
      <div class="message">
        <span class="text">{{ toastMessage }}</span>
      </div>

      <!-- Close Icon -->
      <i class="fas fa-times close" @click="closeToast"></i>

      <!-- Progress Bar -->
      <div class="custom-progress">
        <div class="progress-bar" ref="progressBar"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue';
import gsap from 'gsap';

export default {
  name: 'ToastNotification',
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    message: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      default: 'add', // 'add', 'remove', or 'error'
    },
    duration: {
      type: Number,
      default: 5000, // Duration in milliseconds
    },
  },
  setup(props, { emit }) {
    const toastActive = ref(props.show);
    const toastMessage = ref(props.message);
    const toastType = ref(props.type);
    const progressBar = ref(null);

    let toastTimeout = null;
    let progressBarAnimation = null;

    // Watch for changes in the 'show' prop
    watch(
      () => props.show,
      (newVal) => {
        if (newVal) {
          showToast();
        } else {
          closeToast();
        }
      }
    );

    const showToast = () => {
      // Clear any existing timeout
      if (toastTimeout) {
        clearTimeout(toastTimeout);
        toastTimeout = null;
      }

      // Kill any existing progress bar animation
      if (progressBarAnimation) {
        progressBarAnimation.kill();
        progressBarAnimation = null;
      }

      // Reset progress bar
      if (progressBar.value) {
        gsap.set(progressBar.value, { scaleX: 0 });
      }

      // Set toast content and show it
      toastMessage.value = props.message;
      toastType.value = props.type;
      toastActive.value = true;

      // Animate progress bar using GSAP
      if (progressBar.value) {
        progressBarAnimation = gsap.to(progressBar.value, {
          scaleX: 1,
          transformOrigin: 'left',
          duration: props.duration / 1000,
          ease: 'linear',
        });
      }

      // Set timeout to hide toast after specified duration
      toastTimeout = setTimeout(() => {
        closeToast();
      }, props.duration);
    };

    const closeToast = () => {
      if (toastTimeout) {
        clearTimeout(toastTimeout);
        toastTimeout = null;
      }
      if (progressBarAnimation) {
        progressBarAnimation.kill();
        progressBarAnimation = null;
      }
      toastActive.value = false;
      emit('update:show', false); // Emit event to update parent component
    };

    return {
      toastActive,
      toastMessage,
      toastType,
      progressBar,
      closeToast,
    };
  },
};
</script>

<style scoped>
/* Toast Notification Styles */
.custom-toast {
  position: fixed;
  top: 25px;
  right: 35px;
  border-radius: 12px;
  background: #fff; /* Default background */
  padding: 15px 20px;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  border-left: 6px solid #007bff; /* Default border color */
  overflow: hidden;
  transform: translateX(100%);
  opacity: 0;
  transition: transform 0.5s ease-in-out, opacity 0.5s ease-in-out;
  z-index: 9999;
  min-width: 300px;
}

.custom-toast.active {
  transform: translateX(0);
  opacity: 1;
}

/* Add Type Toast */
.custom-toast.add {
  background: #e6f4ea; /* Light green background */
  border-left-color: #28a745; /* Green border */
}

.custom-toast.add .action-icon {
  background-color: #28a745; /* Green icon background */
}

/* Remove Type Toast */
.custom-toast.remove {
  background: #f8e6e6; /* Light red background */
  border-left-color: #dc3545; /* Red border */
}

.custom-toast.remove .action-icon {
  background-color: #dc3545; /* Red icon background */
}

/* Error Type Toast */
.custom-toast.error {
  background: #f8d7da; /* Light red background for errors */
  border-left-color: #dc3545; /* Red border */
}

.custom-toast.error .action-icon {
  background-color: #dc3545; /* Red icon background */
}

/* Toast Content Layout */
.toast-content {
  display: flex;
  align-items: center;
  position: relative;
}

/* Action Icon Styles */
.toast-content .action-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 35px;
  width: 35px;
  color: #fff;
  font-size: 20px;
  border-radius: 50%;
  margin-right: 15px; /* Space between icon and message */
}

/* Message Styles */
.toast-content .message {
  flex-grow: 1;
  text-align: left;
}

.toast-content .message .text {
  font-size: 16px;
  color: #333;
}

/* Close Icon Styles */
.custom-toast .close {
  position: absolute;
  top: 10px;
  right: 15px;
  padding: 5px;
  cursor: pointer;
  opacity: 0.7;
  background: transparent; /* Ensure no background color */
  border: none;
  color: #666;
  font-size: 14px;
}

.custom-toast .close:hover {
  opacity: 1;
}

/* Progress Bar Styles */
.custom-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  width: 100%;
  background: #ddd;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  width: 100%;
  background-color: #0057d9;
  transform-origin: left;
  transform: scaleX(0); /* Start with scaleX(0) */
}
</style>
