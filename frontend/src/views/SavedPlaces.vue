<template>
    <div>
        <h1>Saved Places</h1>
        <ul>
            <li v-for="place in savedPlaces" :key="place.id">
                {{ place.name }}
            </li>
        </ul>
    </div>
</template>

<script>
export default {
    data() {
        return {
            savedPlaces: [
                { id: 1, name: 'Place 1' },
                { id: 2, name: 'Place 2' },
                { id: 3, name: 'Place 3' }
            ]
        };
    }
};
</script>

<style scoped>
h1 {
    color: #333;
}
ul {
    list-style-type: none;
    padding: 0;
}
li {
    margin-bottom: 10px;
}
</style>