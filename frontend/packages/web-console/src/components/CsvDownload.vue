<template>
    <div>
        <v-btn
            outlined
            class="ml-2 grey darken-3 white--text"
            @click="popupCsvDownload"
        >
            {{ $t('common.downloadCSV') }}
        </v-btn>
        <v-dialog v-model="showPopupCsvDownload" max-width="580">
            <v-card>
                <v-card-title class="text-h5">
                    {{ $t('common.downloadCSV') }}
                    <v-spacer></v-spacer>
                    <v-btn icon @click="showPopupCsvDownload = false">
                        <v-icon>close</v-icon>
                    </v-btn>
                </v-card-title>
                <v-card-text style="color: black">
                    {{ $t('common.downloadCSVVerification') }}
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        class="pa-2"
                        color="grey darken-1"
                        text
                        outlined
                        @click="showPopupCsvDownload = false"
                    >
                        {{ $t('common.cancel') }}
                    </v-btn>
                    <v-btn
                        color="white"
                        class="pa-2 primary"
                        text
                        @click="executionCsvDownload"
                    >
                        OK
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-snackbar v-model="showSnackbar">
            {{ $t('common.snackbarDownloadCSV') }}
            <template v-slot:action="{ attrs }">
                <v-btn icon v-bind="attrs" @click="showSnackbar = false">
                    <v-icon>close</v-icon>
                </v-btn>
            </template>
        </v-snackbar>
    </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';

@Component
export default class CsvDownload extends Vue {
    showPopupCsvDownload = false;
    showSnackbar = false;
    popupCsvDownload(): void {
        this.showPopupCsvDownload = true;
    }
    executionCsvDownload(): void {
        this.showPopupCsvDownload = false;
        this.showSnackbar = true;
    }
}
</script>
