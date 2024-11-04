<!-- src/components/StarRating.vue -->
<template>
    <div class="star-rating">
      <span
        v-for="star in 5"
        :key="star"
        class="star"
        :class="{'filled': star <= fullStars, 'half-filled': star === Math.ceil(rating), 'empty': star > Math.ceil(rating)}"
      >
        ★
      </span>
    </div>
  </template>
  
  <script>
  export default {
    name: "StarRating",
    props: {
      rating: {
        type: Number,
        required: true,
        default: 0,
      },
    },
    computed: {
      fullStars() {
        return Math.floor(this.rating);
      },
      hasHalfStar() {
        return this.rating % 1 >= 0.25 && this.rating % 1 < 0.75;
      },
    },
  };
  </script>
  
  <style scoped>
  .star-rating {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .star {
    font-size: 1rem;
    color: #ccc; /* Default star color */
    margin-right: 2px;
    position: relative;
  }
  
  .star.filled {
    color: #f39c12; /* Highlighted star color */
  }
  
  .star.half-filled::before {
    content: '★';
    position: absolute;
    left: 0;
    width: 50%;
    overflow: hidden;
    color: #f39c12;
  }
  </style>
  