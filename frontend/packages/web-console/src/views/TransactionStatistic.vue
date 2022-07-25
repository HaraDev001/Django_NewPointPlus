<template>
    <v-container fluid class="px-8">
        <div class="pt-6 mb-8">
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
                    {{ $t('transaction.summary') }}
                </v-col>
                <v-spacer></v-spacer>
                <v-col cols="auto">
                    <CsvDownload />
                </v-col>
            </v-row>
        </div>
        <v-row no-gutters class="mt-8">
            <v-tabs>
                <v-tab>{{ $t('transaction.statistic.cardTotal') }}</v-tab>
                <v-tab>
                    {{ $t('transaction.statistic.baseDateUnusedBalance') }}
                </v-tab>
                <v-tab>
                    {{ $t('transaction.statistic.eventAggregation') }}
                </v-tab>
                <v-tab>
                    {{ $t('transaction.statistic.totalNumberMoneyIssued') }}
                </v-tab>
                <v-tab-item>
                    <transaction-statistic-search />
                </v-tab-item>
                <v-tab-item>
                    <transaction-statistic-search />
                </v-tab-item>
                <v-tab-item>
                    <transaction-statistic-search />
                </v-tab-item>
                <v-tab-item>
                    <transaction-statistic-search />
                </v-tab-item>
            </v-tabs>
        </v-row>
    </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import CsvDownload from '../components/CsvDownload.vue';
import TransactionStatisticSearch from './TransactionStatisticSearch.vue';
@Component({ components: { CsvDownload, TransactionStatisticSearch } })
export default class TransactionStatistic extends Vue {}
</script>
