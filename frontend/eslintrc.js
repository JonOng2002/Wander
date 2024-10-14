module.exports = {
    env: {
      browser: true,
      es2021: true,
      'vue/setup-compiler-macros': true // Enable Vue 3 macros like defineProps
    },
    extends: [
      'plugin:vue/vue3-essential',
      'eslint:recommended'
    ],
    parserOptions: {
      ecmaVersion: 12,
      sourceType: 'module'
    },
    plugins: [
      'vue'
    ],
    rules: {
      // Add custom rules if necessary
    }
  };