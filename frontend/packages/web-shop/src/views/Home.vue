<template>
    <hello-world />
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import HelloWorld from '../components/HelloWorld.vue';

@Component({ name: 'Home', components: { HelloWorld } })
export default class Home extends Vue {}
</script>
