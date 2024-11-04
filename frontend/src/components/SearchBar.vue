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
      <button type="submit" class="btn btn-dark btn-lg ms-2">Search!</button>
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
}

/* Expand on load */
.searchInput.animated {
  width: 100%; /* Full width on animation */
  opacity: 1;
}
</style>