<template>
  <div id="app">
    <h1 style="text-align: center; font-family: Helvetica; color: lightcoral;">Video Content Analyzer</h1>
    <UploadVideo />
    <AnalyzeLink />
  </div>
</template>

<script>
// import UploadVideo from './components/UploadVideo.vue'
import AnalyzeLink from './components/AnalyseLink.vue'

export default {
  components: {
    // UploadVideo,
    AnalyzeLink
  }
}
</script>
