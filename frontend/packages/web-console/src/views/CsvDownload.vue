<template>
    <v-container fluid class="px-8">
        <div class="pt-3 mb-10">
            <v-row>
                <v-col
                    cols="12"
                    md="9"
                    class="d-flex flex-row align-center text-h4"
                >
                    <v-row>
                        <v-col
                            cols="auto"
                            class="
                                d-flex
                                flex-row
                                align-center
                                text-h4
                                font-weight-bold
                            "
                        >
                            {{ $t('CSVDownload.title') }}
                        </v-col>
                    </v-row>
                </v-col>
            </v-row>
        </div>
        <div class="mb-8">
            <div class="text-body-2 mb-2">
                {{ $t('CSVDownload.itemTitleContent') }}{{ contentType }}
            </div>
            <div class="text-body-2">
                {{ $t('CSVDownload.itemTitlePeriod') }}{{ period }}
            </div>
            <v-divider class="my-6" />
            <a href="#" class="info--text">
                {{ downloadFile }}{{ $t('CSVDownload.downloadFileRemark') }}
            </a>
            <v-divider class="mt-6" />
            <div class="text-caption text--disabled mt-2">
                {{ $t('CSVDownload.annotationFirstHalf') }}
                {{ annotationPeriod }}
                {{ $t('CSVDownload.annotationSecondHalf') }}
            </div>
        </div>
    </v-container>
</template>
<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';

@Component
export default class CsvDownload extends Vue {
    contentType = '取引履歴';
    period = '2021/07/01 〜 07/30';
    downloadFile = '20210730_取引履歴.zip';
    annotationPeriod = '2021/08/03 20:32';
}
</script>
