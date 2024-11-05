<template>
  <div class="search-bar-container d-flex justify-content-center">
    <form @submit.prevent="submitLink" class="search-form">
      <input
        type="text"
        v-model="link"
        class="form-control searchInput"
        :placeholder="currentPlaceholder"
        required
        :disabled="isLoading"
      />
      <button id="searchQuerySubmit" type="submit" name="searchQuerySubmit">
      <svg style="width:24px;height:24px" viewBox="0 0 24 24"><path fill="#666666" d="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z" />
      </svg>
    </button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'SearchBar',
  props: {
    tiktokLink: {
      type: String,
      default: ''
    },
    isLoading: {
    type: Boolean,
    default: false
  }
  },
  data() {
    return {
      link: this.tiktokLink,
      currentPlaceholder: '', // Current placeholder that is being animated
      placeholders: [
        'Paste a Tiktok Link here!',
        'Search for TikTok Japan',
        'Search for TikTok Thailand',
        'Search for TikTok USA',
        'Search for TikTok England',
        'Search for TikTok Australia'
      ],
      placeholderIndex: 0,
      MIN_ANIMATION_DELAY: 50, // Minimum delay between adding letters
      MAX_ANIMATION_DELAY: 90, // Maximum delay between adding letters
      DELAY_AFTER_ANIMATION: 1000, // Delay after the animation ends
    };
  },
  mounted() {
    this.animatePlaceholder(); // Start animating the placeholder
    this.$nextTick(() => {
    setTimeout(() => {
      const searchInput = this.$el.querySelector('.searchInput');
      searchInput.classList.add('animated');
    }, 100); // Delay to ensure the element is visible before animation
  });
  },
  beforeUnmount() {
    clearInterval(this.placeholderInterval); // Clear any running intervals on component unmount
  },
  methods: {
    submitLink() {
      this.$emit('submit-link', this.link);
    },
    getRandomDelayBetween(min, max) {
      return Math.floor(Math.random() * (max - min + 1)) + min;
    },
    setPlaceholder(inputNode, placeholderText) {
      inputNode.placeholder = placeholderText;
    },
    animateLetters(currentLetters, remainingLetters, inputNode, onAnimationEnd) {
      if (!remainingLetters.length) {
        return (
          typeof onAnimationEnd === 'function' &&
          onAnimationEnd(currentLetters.join(''), inputNode)
        );
      }

      currentLetters.push(remainingLetters.shift());

      setTimeout(() => {
        this.setPlaceholder(inputNode, currentLetters.join(''));
        this.animateLetters(currentLetters, remainingLetters, inputNode, onAnimationEnd);
      }, this.getRandomDelayBetween(this.MIN_ANIMATION_DELAY, this.MAX_ANIMATION_DELAY));
    },
    onAnimationEnd(placeholder, inputNode) {
      setTimeout(() => {
        let newPlaceholder = '';

        // Ensure we pick a new placeholder that is different from the current one
        do {
          this.placeholderIndex = (this.placeholderIndex + 1) % this.placeholders.length;
          newPlaceholder = this.placeholders[this.placeholderIndex];
        } while (placeholder === newPlaceholder);

        // Animate the new placeholder
        this.animatePlaceholder(inputNode, newPlaceholder, this.onAnimationEnd);
      }, this.DELAY_AFTER_ANIMATION);
    },
    animatePlaceholder() {
      const inputNode = this.$el.querySelector('.searchInput');
      this.animateLetters([], [...this.placeholders[this.placeholderIndex]], inputNode, this.onAnimationEnd);
    }
  }
};
</script>
<style scoped>
.search-bar-container {
  display: flex;
  justify-content: center;
  margin-top: -1rem;
}

.search-form {
  display: flex;
  width: 100%;
  justify-content: center;
  
}

.searchInput {
  width: 20px; /* Start with a small width to visualize expansion */
  opacity: 0;
  transform-origin: center;
  transition: width 0.6s ease-in-out, opacity 0.6s ease-in-out;
  border-radius: 1.625rem;
  background: #f5f5f5;
}

/* Expand on load */
.searchInput.animated {
  width: 100%; /* Full width on animation */
  opacity: 1;
}
#searchQuerySubmit {
  width: 3.5rem;
  height: 2.8rem;
  margin-left: -3.5rem;
  background: none;
  border: none;
  outline: none;
}
</style>