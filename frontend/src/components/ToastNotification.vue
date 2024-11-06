<!-- frontend/src/components/ToastNotification.vue -->

<template>
  <div :class="['custom-toast', { active: toastActive, exit: !toastActive }, toastType]">
    <i class="fas fa-times close" @click="closeToast"></i>
    <div class="toast-content">
      <!-- Action Icon -->
      <i
        :class="[ 
          'fas',
          toastType === 'add'
            ? 'fa-check'
            : toastType === 'remove'
            ? 'fa-times'
            : 'fa-info',
          'action-icon',
        ]"
      ></i>

      <!-- Message -->
      <div class="message">
        <span class="text">{{ toastMessage }}</span>
      </div>

      <!-- Close Icon -->
      
    </div>

    <!-- Progress Bar -->
    <div class="custom-progress">
      <div class="progress-bar" ref="progressBar"></div>
    </div>
  </div>
</template>

<script>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue';
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
      default: 'add', // 'add', 'remove', or 'info'
    },
    duration: {
      type: Number,
      default: 3000, // Duration in milliseconds (3 seconds)
    },
  },
  setup(props, { emit }) {
    const toastActive = ref(false);
    const toastMessage = ref(props.message);
    const toastType = ref(props.type);
    const progressBar = ref(null);

    let toastTimeout = null;
    let progressBarAnimation = null;

    const showToast = () => {
      if (toastTimeout) clearTimeout(toastTimeout);
      if (progressBarAnimation) progressBarAnimation.kill();

      if (progressBar.value) {
        gsap.set(progressBar.value, { scaleX: 0 });
      }

      toastMessage.value = props.message;
      toastType.value = props.type;
      toastActive.value = true;

      if (progressBar.value) {
        progressBarAnimation = gsap.to(progressBar.value, {
          scaleX: 1,
          transformOrigin: 'left',
          duration: props.duration / 1000,
          ease: 'linear',
        });
      }

      toastTimeout = setTimeout(() => {
        closeToast();
      }, props.duration);
    };

    const closeToast = () => {
      if (toastTimeout) clearTimeout(toastTimeout);
      if (progressBarAnimation) progressBarAnimation.kill();

      toastActive.value = false;
      setTimeout(() => emit('update:show', false), 500); // Delay for exit animation
    };

    watch(() => props.show, (newVal) => {
      if (newVal) {
        showToast();
      } else {
        closeToast();
      }
    });

    onBeforeUnmount(() => {
      if (toastTimeout) clearTimeout(toastTimeout);
      if (progressBarAnimation) progressBarAnimation.kill();
    });

    onMounted(() => {
      if (props.show) {
        showToast();
      }
    });

    return { toastActive, toastMessage, toastType, progressBar, closeToast };
  },
};
</script>

<style scoped>
.custom-toast {
  position: fixed;
  top: 25px;
  right: 35px;
  border-radius: 12px;
  background: #fff;
  padding: 20px 35px 20px 25px;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  border-left: 6px solid #007bff;
  overflow: hidden;
  transform: translateX(100%);
  opacity: 0;
  transition: transform 0.5s ease-in-out, opacity 0.5s ease-in-out;
  z-index: 9999;
}

.custom-toast.active {
  transform: translateX(0);
  opacity: 1;
}

.custom-toast.exit {
  transform: translateX(100%);
  opacity: 0;
}

.custom-toast.add {
  background: #e6f4ea;
  border-left-color: #28a745;
}

.custom-toast.add .action-icon {
  background-color: #28a745;
}

.custom-toast.remove {
  background: #f8e6e6;
  border-left-color: #dc3545;
}

.custom-toast.remove .action-icon {
  background-color: #dc3545;
}

.custom-toast.info {
  background: #e6f0fa;
  border-left-color: #17a2b8;
}

.custom-toast.info .action-icon {
  background-color: #17a2b8;
}

.toast-content {
  display: flex;
  align-items: center;
  position: relative;
  padding-right: 30px; /* Space for the close icon */
}

.toast-content .action-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 35px;
  width: 35px;
  color: #fff;
  font-size: 20px;
  border-radius: 50%;
  flex-shrink: 0; /* Prevent the icon from being squished */
}

.toast-content .message {
  display: flex;
  flex-direction: column;
  margin: 0 10px 0 20px;
}

.toast-content .message .text {
  font-size: 20px;
  font-weight: 600;
  font-family: 'Source Sans 3', sans-serif;
  color: #333333;
}

.custom-toast .close {
  position: absolute;
  top: 10px; /* Adjusts distance from the top of the container */
  right: 1rem; /* Adjusts distance from the right of the container */
  padding: 5px;
  cursor: pointer;
  opacity: 0.7;
  background: transparent;
  border: none;
  color: #666;
  font-size: 16px;
}

.custom-toast .close:hover {
  opacity: 1;
}

.custom-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 4px;
  width: 100%;
  background: #ddd;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  width: 100%;
  background-color: #0057d9;
  transform-origin: left;
  transform: scaleX(0);
}

/* Media Queries for Responsiveness */

/* Medium screens (max-width: 1024px) */
@media (max-width: 1024px) {
  .custom-toast {
    right: 20px;
    padding: 15px 25px 15px 20px;
    max-width: 350px;
  }

  .toast-content .message .text {
    font-size: 14px;
  }

  .custom-toast .close {
    font-size: 14px;
    top: 8px;
    right: 8px;
  }
}

/* Small screens (max-width: 768px) */
@media (max-width: 768px) {
  .custom-toast {
    right: 15px;
    padding: 12px 20px 12px 15px;
    max-width: 300px;
  }

  .toast-content .action-icon {
    height: 30px;
    width: 30px;
    font-size: 18px;
  }

  .toast-content .message .text {
    font-size: 15px;
  }

  .custom-toast .close {
    font-size: 14px;
    top: 8px;
    right: 8px;
  }
}

/* Extra small screens (max-width: 576px) */
@media (max-width: 576px) {
  .custom-toast {
    right: 10px;
    padding: 10px 15px 10px 10px;
    max-width: 250px;
  }

  .toast-content .action-icon {
    height: 25px;
    width: 25px;
    font-size: 14px;
    min-width: 25px; /* Maintain aspect ratio */
    min-height: 25px; /* Maintain aspect ratio */
  }

  .toast-content .message .text {
    font-size: 14px;
  }

  .custom-toast .close {
    font-size: 15px;
    top: 5px;
    right: 5px;
  }
}
</style>
