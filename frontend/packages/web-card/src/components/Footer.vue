<template>
    <v-footer class="transparent" padless>
        <v-row no-gutters>
            <v-col class="text-center text-caption pb-4" cols="12">
                ©️2021 {{ providerName }}
            </v-col>
        </v-row>
    </v-footer>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { mapGetters } from 'vuex';

@Component({
    computed: {
        ...mapGetters(['providerName']),
    },
})
export default class Footer extends Vue {
    protected providerName!: string;
}
</script>
