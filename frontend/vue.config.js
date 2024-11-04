const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/api': {
        target: 'https://maps.googleapis.com',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '/maps/api', // Correctly map '/api' to '/maps/api'
        },
      },
    },
  },
});
