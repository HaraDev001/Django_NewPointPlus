<template>
    <v-app>
        <layout-header></layout-header>
        <router-view></router-view>
        <layout-footer></layout-footer>
    </v-app>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import LayoutHeader from '../components/Header.vue';
import LayoutFooter from '../components/Footer.vue';

@Component({ components: { LayoutHeader, LayoutFooter } })
export default class BaseLayout extends Vue {}
</script>
