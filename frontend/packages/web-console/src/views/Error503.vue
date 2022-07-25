<template>
    <v-app class="grey lighten-5">
        <v-app-bar
            app
            flat
            elevation="1"
            color="white"
            class="d-flex justify-center"
        >
            <div class="d-flex align-center">
                <v-img src="~@/assets/cmn/logo.svg" width="132"></v-img>
            </div>
        </v-app-bar>
        <v-container fill-height>
            <v-sheet
                max-width="500"
                color="transparent"
                class="ma-auto text-center"
            >
                <div>
                    <div class="text-h5 font-weight-bold">
                        {{ $t('error.503.title') }}
                    </div>
                    <div
                        class="
                            text--secondary
                            font-weight-bold
                            text-body-1
                            pt-1
                        "
                    >
                        {{ $t('error.common.codeItemTitle') }}
                        {{ $t('error.503.code') }}
                    </div>
                </div>
                <div
                    class="text--secondary text-left pt-6"
                    v-html="$t('error.503.text')"
                ></div>
                <div class="pt-8">
                    <v-btn color="grey lighten-2" elevation="0">
                        {{ $t('error.common.goToback') }}
                    </v-btn>
                </div>
            </v-sheet>
        </v-container>
        <layout-footer></layout-footer>
    </v-app>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import LayoutFooter from '../components/Footer.vue';

@Component({
    components: { LayoutFooter },
})
export default class Error503 extends Vue {}
</script>
