<template>
    <v-footer padless inset color="transparent">
        <div class="text-center text-body-2 text--secondary mx-auto py-4">
            &copy; arara inc.
        </div>
    </v-footer>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';

@Component
export default class LayoutFooter extends Vue {}
</script>
