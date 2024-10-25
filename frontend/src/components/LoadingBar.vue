<template>
    <div class="loading-bar" v-if="isLoading">
        <div class="bar"></div>
    </div>
</template>

<script>
export default {
    props: {
        isLoading: {
            type: Boolean,
            required: true
        }
    }
}
</script>

<style scoped>
.loading-bar {
    position: relative;
    width: 100%;
    height: 4px;
    background-color: #f0f0f0;
}

.bar {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    background-color: #007bff;
    animation: loading 2s infinite;
}

@keyframes loading {
    0% {
        width: 0;
    }

    100% {
        width: 100%;
    }
}
</style>