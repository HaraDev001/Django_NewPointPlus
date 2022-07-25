<template>
    <v-container fluid class="px-8">
        <div class="pt-3 mb-10">
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
                    {{ $t('transaction.historyList') }}
                </v-col>
                <v-spacer></v-spacer>
                <v-col cols="auto">
                    <CsvDownload />
                </v-col>
            </v-row>
        </div>
        <v-row no-gutters align="center" style="width: 900px">
            <v-col class="pa-0 pr-2">
                <v-select
                    full-width
                    dense
                    :label="$t('transaction.aggregationPeriod')"
                    outlined
                    hide-details
                    :items="listPeriod"
                ></v-select>
            </v-col>
            <v-col class="pa-0 pl-2">
                <v-menu
                    ref="menu1"
                    v-model="menu1"
                    :close-on-content-click="false"
                    transition="scale-transition"
                    offset-y
                    min-width="auto"
                >
                    <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                            v-model="dateFormatted"
                            :label="$t('transaction.history.startDate')"
                            readonly
                            outlined
                            dense
                            hide-details
                            class="select-datepicker"
                            v-bind="attrs"
                            placeholder="2021/07/01"
                            persistent-placeholder
                            v-on="on"
                        ></v-text-field>
                    </template>
                    <v-date-picker
                        v-model="date1"
                        no-title
                        @input="menu1 = false"
                    ></v-date-picker>
                </v-menu>
            </v-col>
            <v-col cols="auto" class="pa-0 px-2">〜</v-col>
            <v-col class="pa-0 pr-2">
                <v-menu
                    ref="menu2"
                    v-model="menu2"
                    :close-on-content-click="false"
                    transition="scale-transition"
                    offset-y
                    min-width="auto"
                >
                    <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                            v-model="dateFormatted2"
                            :label="$t('transaction.history.endDate')"
                            readonly
                            outlined
                            dense
                            hide-details
                            class="select-datepicker"
                            v-bind="attrs"
                            placeholder="2021/07/31"
                            persistent-placeholder
                            v-on="on"
                        ></v-text-field>
                    </template>
                    <v-date-picker
                        v-model="date2"
                        no-title
                        @input="menu2 = false"
                    ></v-date-picker>
                </v-menu>
            </v-col>
            <v-col cols="auto" class="py-0 px-2">
                <v-divider vertical style="height: 40px"></v-divider>
            </v-col>
            <v-col
                cols="auto"
                class="text-body-2 grey--text text--darken-2 text-right px-2"
            >
                {{ $t('card.cardDisplayType') }}：
            </v-col>
            <v-radio-group
                v-model="radios"
                row
                class="font-weight-bold mt-0 pt-0"
                mandatory
                hide-details
            >
                <v-radio
                    :label="$t('card.cardProduction')"
                    value="radio-1"
                ></v-radio>
                <v-radio :label="$t('card.cardTest')" value="radio-2"></v-radio>
            </v-radio-group>
        </v-row>
        <v-divider class="my-6"></v-divider>
        <v-row no-gutters align="center" style="width: 1055px">
            <v-col class="pa-0 col-2">
                <v-select
                    v-model="listTransactionTypeSelected"
                    full-width
                    dense
                    :label="$t('transaction.transactionType')"
                    outlined
                    hide-details="auto"
                    :items="listTransactionType"
                    multiple
                >
                    <template v-slot:selection="{ item, index }">
                        <div
                            v-if="listTransactionTypeSelected.length === 1"
                            class="
                                v-select__selection v-select__selection--comma
                            "
                        >
                            {{ item }}
                        </div>
                        <span
                            v-if="index === 1"
                            class="
                                v-select__selection v-select__selection--comma
                            "
                        >
                            {{ listTransactionTypeSelected.length }}件選択
                        </span>
                    </template>
                </v-select>
            </v-col>
            <v-col cols="auto" class="py-0 px-4">
                <v-divider vertical style="height: 40px"></v-divider>
            </v-col>
            <v-col class="pa-0 col-2">
                <v-select
                    v-model="listTerminalTypeSelected"
                    full-width
                    dense
                    :label="$t('transaction.history.terminalType')"
                    outlined
                    hide-details="auto"
                    :items="listTerminalType"
                    multiple
                >
                    <template v-slot:selection="{ item, index }">
                        <div
                            v-if="listTerminalTypeSelected.length === 1"
                            class="
                                v-select__selection v-select__selection--comma
                            "
                        >
                            {{ item }}
                        </div>
                        <span
                            v-if="index === 1"
                            class="
                                v-select__selection v-select__selection--comma
                            "
                        >
                            {{ listTerminalTypeSelected.length }}件選択
                        </span>
                    </template>
                </v-select>
            </v-col>
            <v-col cols="auto" class="py-0 px-4">
                <v-divider vertical style="height: 40px"></v-divider>
            </v-col>
            <v-col class="pa-0 pr-1">
                <v-select
                    dense
                    :label="$t('transaction.history.targetCompany')"
                    outlined
                    hide-details
                    multiple
                ></v-select>
            </v-col>
            <v-col class="pa-0 pl-1">
                <v-select
                    dense
                    :label="$t('transaction.history.targetStore')"
                    outlined
                    hide-details
                    multiple
                ></v-select>
            </v-col>
            <v-col cols="auto" class="py-0 px-4">
                <v-divider vertical style="height: 40px"></v-divider>
            </v-col>
            <v-col class="pa-0 pr-1">
                <v-select
                    dense
                    :label="$t('card.cardSettingName')"
                    outlined
                    hide-details
                    multiple
                ></v-select>
            </v-col>
            <v-col class="pa-0 pl-1 col-2">
                <v-select
                    v-model="listCardStatusSelected"
                    full-width
                    dense
                    :label="$t('card.cardStatus')"
                    outlined
                    hide-details
                    :items="listCardStatus"
                    multiple
                >
                    <template v-slot:selection="{ item, index }">
                        <div
                            v-if="listCardStatusSelected.length === 1"
                            class="
                                v-select__selection v-select__selection--comma
                            "
                        >
                            {{ item }}
                        </div>
                        <span
                            v-if="index === 1"
                            class="
                                v-select__selection v-select__selection--comma
                            "
                        >
                            {{ listCardStatusSelected.length }}件選択
                        </span>
                    </template>
                </v-select>
            </v-col>
        </v-row>
        <v-row no-gutters class="pt-4" style="width: 365px" align="center">
            <v-col cols="8" class="pr-2">
                <v-text-field
                    :placeholder="$t('card.cardNumber')"
                    outlined
                    dense
                    hide-details
                ></v-text-field>
            </v-col>
            <v-col cols="4" style="height: 40px">
                <v-btn
                    color="grey lighten-2"
                    class="grey darken-4--text py-4"
                    height="40"
                    block
                    elevation="0"
                >
                    {{ $t('common.uploadCSV') }}
                </v-btn>
            </v-col>
        </v-row>
        <v-divider class="my-6"></v-divider>
        <v-row no-gutters class="mx-auto mb-8" style="width: 156px">
            <v-col cols="5" class="pa-0 mr-2">
                <v-btn
                    class="pa-2"
                    color="grey darken-1"
                    height="40"
                    block
                    elevation="0"
                    outlined
                >
                    {{ $t('common.clear') }}
                </v-btn>
            </v-col>
            <v-col class="pa-0">
                <v-btn
                    color="white"
                    class="pa-2 primary"
                    height="40"
                    block
                    elevation="0"
                >
                    {{ $t('common.search') }}
                </v-btn>
            </v-col>
        </v-row>
        <v-card outlined class="mt-8">
            <v-data-table
                v-model="selected"
                checkbox-color="primary"
                :headers="headers"
                :items="promotions"
                :items-per-page="10"
                :footer-props="{
                    'items-per-page-options': [10, 20, 30, 50, 100],
                    'items-per-page-text': this.$t('common.itemsPerPageText'),
                }"
                item-key="transactionId"
                style="white-space: nowrap"
                show-select
            >
                <template v-slot:[`header.data-table-select`]="{ props, on }">
                    <v-simple-checkbox
                        :value="props.value || props.indeterminate"
                        :indeterminate="props.indeterminate"
                        :ripple="false"
                        color="primary"
                        v-on="on"
                    />
                </template>
                <template v-slot:top>
                    <v-menu
                        v-if="selected.length > 0"
                        v-model="showPopupSelect"
                        :close-on-click="false"
                        :close-on-content-click="false"
                        :nudge-width="100"
                        offset-y
                        max-width="15%"
                    >
                        <template v-slot:activator="{ attrs }">
                            <v-btn
                                class="ma-3"
                                color="grey lighten-2"
                                v-bind="attrs"
                                elevation="0"
                                small
                                @click="popupConfirm"
                            >
                                {{ $t('transaction.transactionCancellation') }}
                            </v-btn>
                        </template>
                    </v-menu>
                    <v-divider></v-divider>
                </template>
                <template v-slot:[`footer.page-text`]="items">
                    {{ items.pageStart }} - {{ items.pageStop }} /
                    {{ items.itemsLength }}
                </template>
                <template v-slot:[`item.date`]="{ item }">
                    {{ item.date }}
                    <v-chip
                        v-if="checkInTransaction(item)"
                        class="ma-2"
                        color="primary"
                        outlined
                    >
                        {{ $t('common.cancelApprovalWaiting') }}i
                        <span class="material-icons">delete</span>
                    </v-chip>
                </template>
            </v-data-table>
        </v-card>
        <v-dialog v-model="showPopupConfirm" max-width="580">
            <v-card>
                <v-card-title class="text-h5">
                    {{ $t('transaction.transactionConfirmCancellation') }}
                    <v-spacer></v-spacer>
                    <v-btn icon @click="showPopupConfirm = false">
                        <v-icon>close</v-icon>
                    </v-btn>
                </v-card-title>
                <v-card-text style="color: black">
                    {{ $t('transaction.transactionApprovalRequest') }}
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        class="pa-2"
                        color="grey darken-1"
                        text
                        outlined
                        @click="showPopupConfirm = false"
                    >
                        {{ $t('common.cancel') }}
                    </v-btn>
                    <v-btn
                        color="white"
                        class="pa-2 primary"
                        text
                        @click="countSelected"
                    >
                        OK
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script lang="ts">
import { Vue, Component, Watch } from 'vue-property-decorator';
import { HistoryItem } from '../models/HistoryModel';
import CsvDownload from '../components/CsvDownload.vue';
@Component({ components: { CsvDownload } })
export default class History extends Vue {
    headers = [
        {
            text: this.$t('transaction.transactionDateTime'),
            align: 'start',
            value: 'date',
            sortable: false,
        },
        {
            text: this.$t('transaction.transactionType'),
            value: 'transactionType',
            sortable: false,
        },
        {
            text: this.$t('transaction.transactionStatus'),
            value: 'transactionStatus',
            sortable: false,
        },
        {
            text: this.$t('transaction.transactionNumber'),
            value: 'transactionId',
            sortable: false,
        },
        {
            text: this.$t('card.cardSettingName'),
            value: 'cardName',
            sortable: false,
        },
        {
            text: this.$t('card.cardSettingType'),
            value: 'cardType',
            sortable: false,
        },
        {
            text: this.$t('card.cardNumber'),
            value: 'cardId',
            sortable: false,
        },
        {
            text: this.$t('transaction.transactionAmount'),
            value: 'amount',
            sortable: false,
            align: 'right',
        },
        {
            text: this.$t('transaction.eventName'),
            value: 'event',
            sortable: false,
        },
        {
            text: this.$t('transaction.history.grantAmountOrNumber'),
            value: 'grant',
            sortable: false,
            align: 'right',
        },
        {
            text: this.$t('transaction.history.grantDateTime'),
            value: 'grantDate',
            sortable: false,
        },
        {
            text: this.$t('transaction.history.companyName'),
            value: 'company',
            sortable: false,
        },
        {
            text: this.$t('transaction.history.storeName'),
            value: 'store',
            sortable: false,
        },
        {
            text: this.$t('transaction.history.terminalType'),
            value: 'terminalType',
            sortable: false,
        },
        {
            text: this.$t('transaction.history.terminalNumber'),
            value: 'terminalId',
            sortable: false,
        },
    ];
    promotions = [
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ',
            transactionStatus: '完了',
            transactionId: '123456',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678901111',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/27 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '南青山店',
            terminalType: 'チャージ機',
            terminalId: 'a1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ取消',
            transactionStatus: '完了',
            transactionId: '678901',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678902222',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/26 23:59:54',
            company: '株式会社ポッカクリエイト',
            store: '松戸店',
            terminalType: 'POS',
            terminalId: 'bbbb1234',
        },
        {
            date: '2021/6/25 13:36:56',
            transactionType: '付与',
            transactionStatus: '完了',
            transactionId: '234567',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/27 23:54:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1234ccc',
        },
        {
            date: '2021/6/25 13:54:56',
            transactionType: '付与取消',
            transactionStatus: '完了',
            transactionId: '345678',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1d2d3d4d',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: '決済',
            transactionStatus: '完了',
            transactionId: '456789',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678905555',
            amount: '1,000',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/29 23:59:59',
            company: 'オリエンタルランド株式会社',
            store: '浦安店',
            terminalType: 'マルチ決済端末',
            terminalId: 'aaaaa09826482',
        },
        {
            date: '2021/6/27 12:34:56',
            transactionType: '決済取消',
            transactionStatus: '完了',
            transactionId: '567890',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678906666',
            amount: '1,500',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社フレーベル館',
            store: '北千住店',
            terminalType: 'マルチ決済機',
            terminalId: 'hsga1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ',
            transactionStatus: '完了',
            transactionId: '1234567',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678901111',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/27 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '南青山店',
            terminalType: 'チャージ機',
            terminalId: 'a1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ取消',
            transactionStatus: '完了',
            transactionId: '6789017',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678902222',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/26 23:59:54',
            company: '株式会社ポッカクリエイト',
            store: '松戸店',
            terminalType: 'POS',
            terminalId: 'bbbb1234',
        },
        {
            date: '2021/6/25 13:36:56',
            transactionType: '付与',
            transactionStatus: '完了',
            transactionId: '2345677',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/27 23:54:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1234ccc',
        },
        {
            date: '2021/6/25 13:54:56',
            transactionType: '付与取消',
            transactionStatus: '完了',
            transactionId: '3456787',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1d2d3d4d',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: '決済',
            transactionStatus: '完了',
            transactionId: '4567897',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678905555',
            amount: '1,000',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/29 23:59:59',
            company: 'オリエンタルランド株式会社',
            store: '浦安店',
            terminalType: 'マルチ決済端末',
            terminalId: 'aaaaa09826482',
        },
        {
            date: '2021/6/27 12:34:56',
            transactionType: '決済取消',
            transactionStatus: '完了',
            transactionId: '5678907',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678906666',
            amount: '1,500',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社フレーベル館',
            store: '北千住店',
            terminalType: 'マルチ決済機',
            terminalId: 'hsga1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ',
            transactionStatus: '完了',
            transactionId: '1234501',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678901111',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/27 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '南青山店',
            terminalType: 'チャージ機',
            terminalId: 'a1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ取消',
            transactionStatus: '完了',
            transactionId: '6789002',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678902222',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/26 23:59:54',
            company: '株式会社ポッカクリエイト',
            store: '松戸店',
            terminalType: 'POS',
            terminalId: 'bbbb1234',
        },
        {
            date: '2021/6/25 13:36:56',
            transactionType: '付与',
            transactionStatus: '完了',
            transactionId: '2345603',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/27 23:54:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1234ccc',
        },
        {
            date: '2021/6/25 13:54:56',
            transactionType: '付与取消',
            transactionStatus: '完了',
            transactionId: '3456704',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1d2d3d4d',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: '決済',
            transactionStatus: '完了',
            transactionId: '4567805',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678905555',
            amount: '1,000',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/29 23:59:59',
            company: 'オリエンタルランド株式会社',
            store: '浦安店',
            terminalType: 'マルチ決済端末',
            terminalId: 'aaaaa09826482',
        },
        {
            date: '2021/6/27 12:34:56',
            transactionType: '決済取消',
            transactionStatus: '完了',
            transactionId: '5678906',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678906666',
            amount: '1,500',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社フレーベル館',
            store: '北千住店',
            terminalType: 'マルチ決済機',
            terminalId: 'hsga1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ',
            transactionStatus: '完了',
            transactionId: '12345607',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678901111',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/27 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '南青山店',
            terminalType: 'チャージ機',
            terminalId: 'a1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ取消',
            transactionStatus: '完了',
            transactionId: '67890108',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678902222',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/26 23:59:54',
            company: '株式会社ポッカクリエイト',
            store: '松戸店',
            terminalType: 'POS',
            terminalId: 'bbbb1234',
        },
        {
            date: '2021/6/25 13:36:56',
            transactionType: '付与',
            transactionStatus: '完了',
            transactionId: '23456709',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/27 23:54:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1234ccc',
        },
        {
            date: '2021/6/25 13:54:56',
            transactionType: '付与取消',
            transactionStatus: '完了',
            transactionId: '3456710',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1d2d3d4d',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: '決済',
            transactionStatus: '完了',
            transactionId: '4567811',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678905555',
            amount: '1,000',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/29 23:59:59',
            company: 'オリエンタルランド株式会社',
            store: '浦安店',
            terminalType: 'マルチ決済端末',
            terminalId: 'aaaaa09826482',
        },
        {
            date: '2021/6/27 12:34:56',
            transactionType: '決済取消',
            transactionStatus: '完了',
            transactionId: '5678912',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678906666',
            amount: '1,500',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社フレーベル館',
            store: '北千住店',
            terminalType: 'マルチ決済機',
            terminalId: 'hsga1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ',
            transactionStatus: '完了',
            transactionId: '1234513',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678901111',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/27 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '南青山店',
            terminalType: 'チャージ機',
            terminalId: 'a1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ取消',
            transactionStatus: '完了',
            transactionId: '6789014',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678902222',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/26 23:59:54',
            company: '株式会社ポッカクリエイト',
            store: '松戸店',
            terminalType: 'POS',
            terminalId: 'bbbb1234',
        },
        {
            date: '2021/6/25 13:36:56',
            transactionType: '付与',
            transactionStatus: '完了',
            transactionId: '2345615',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/27 23:54:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1234ccc',
        },
        {
            date: '2021/6/25 13:54:56',
            transactionType: '付与取消',
            transactionStatus: '完了',
            transactionId: '3456716',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1d2d3d4d',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: '決済',
            transactionStatus: '完了',
            transactionId: '4567817',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678905555',
            amount: '1,000',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/29 23:59:59',
            company: 'オリエンタルランド株式会社',
            store: '浦安店',
            terminalType: 'マルチ決済端末',
            terminalId: 'aaaaa09826482',
        },
        {
            date: '2021/6/27 12:34:56',
            transactionType: '決済取消',
            transactionStatus: '完了',
            transactionId: '5678918',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678906666',
            amount: '1,500',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社フレーベル館',
            store: '北千住店',
            terminalType: 'マルチ決済機',
            terminalId: 'hsga1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ',
            transactionStatus: '完了',
            transactionId: '12345619',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678901111',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/27 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '南青山店',
            terminalType: 'チャージ機',
            terminalId: 'a1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ取消',
            transactionStatus: '完了',
            transactionId: '67890120',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678902222',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/26 23:59:54',
            company: '株式会社ポッカクリエイト',
            store: '松戸店',
            terminalType: 'POS',
            terminalId: 'bbbb1234',
        },
        {
            date: '2021/6/25 13:36:56',
            transactionType: '付与',
            transactionStatus: '完了',
            transactionId: '23456721',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/27 23:54:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1234ccc',
        },
        {
            date: '2021/6/25 13:54:56',
            transactionType: '付与取消',
            transactionStatus: '完了',
            transactionId: '3456722',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1d2d3d4d',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: '決済',
            transactionStatus: '完了',
            transactionId: '4567823',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678905555',
            amount: '1,000',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/29 23:59:59',
            company: 'オリエンタルランド株式会社',
            store: '浦安店',
            terminalType: 'マルチ決済端末',
            terminalId: 'aaaaa09826482',
        },
        {
            date: '2021/6/27 12:34:56',
            transactionType: '決済取消',
            transactionStatus: '完了',
            transactionId: '5678924',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678906666',
            amount: '1,500',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社フレーベル館',
            store: '北千住店',
            terminalType: 'マルチ決済機',
            terminalId: 'hsga1a2a3a4',
        },

        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ',
            transactionStatus: '完了',
            transactionId: '1234525',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678901111',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/27 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '南青山店',
            terminalType: 'チャージ機',
            terminalId: 'a1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ取消',
            transactionStatus: '完了',
            transactionId: '6789026',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678902222',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/26 23:59:54',
            company: '株式会社ポッカクリエイト',
            store: '松戸店',
            terminalType: 'POS',
            terminalId: 'bbbb1234',
        },
        {
            date: '2021/6/25 13:36:56',
            transactionType: '付与',
            transactionStatus: '完了',
            transactionId: '2345627',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/27 23:54:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1234ccc',
        },
        {
            date: '2021/6/25 13:54:56',
            transactionType: '付与取消',
            transactionStatus: '完了',
            transactionId: '3456728',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1d2d3d4d',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: '決済',
            transactionStatus: '完了',
            transactionId: '4567829',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678905555',
            amount: '1,000',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/29 23:59:59',
            company: 'オリエンタルランド株式会社',
            store: '浦安店',
            terminalType: 'マルチ決済端末',
            terminalId: 'aaaaa09826482',
        },
        {
            date: '2021/6/27 12:34:56',
            transactionType: '決済取消',
            transactionStatus: '完了',
            transactionId: '5678930',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678906666',
            amount: '1,500',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社フレーベル館',
            store: '北千住店',
            terminalType: 'マルチ決済機',
            terminalId: 'hsga1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ',
            transactionStatus: '完了',
            transactionId: '12345631',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678901111',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/27 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '南青山店',
            terminalType: 'チャージ機',
            terminalId: 'a1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ取消',
            transactionStatus: '完了',
            transactionId: '67890132',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678902222',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/26 23:59:54',
            company: '株式会社ポッカクリエイト',
            store: '松戸店',
            terminalType: 'POS',
            terminalId: 'bbbb1234',
        },
        {
            date: '2021/6/25 13:36:56',
            transactionType: '付与',
            transactionStatus: '完了',
            transactionId: '23456733',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/27 23:54:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1234ccc',
        },
        {
            date: '2021/6/25 13:54:56',
            transactionType: '付与取消',
            transactionStatus: '完了',
            transactionId: '3456734',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1d2d3d4d',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: '決済',
            transactionStatus: '完了',
            transactionId: '4567835',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678905555',
            amount: '1,000',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/29 23:59:59',
            company: 'オリエンタルランド株式会社',
            store: '浦安店',
            terminalType: 'マルチ決済端末',
            terminalId: 'aaaaa09826482',
        },
        {
            date: '2021/6/27 12:34:56',
            transactionType: '決済取消',
            transactionStatus: '完了',
            transactionId: '5678936',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678906666',
            amount: '1,500',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社フレーベル館',
            store: '北千住店',
            terminalType: 'マルチ決済機',
            terminalId: 'hsga1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ',
            transactionStatus: '完了',
            transactionId: '1234537',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678901111',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/27 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '南青山店',
            terminalType: 'チャージ機',
            terminalId: 'a1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ取消',
            transactionStatus: '完了',
            transactionId: '6789038',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678902222',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/26 23:59:54',
            company: '株式会社ポッカクリエイト',
            store: '松戸店',
            terminalType: 'POS',
            terminalId: 'bbbb1234',
        },
        {
            date: '2021/6/25 13:36:56',
            transactionType: '付与',
            transactionStatus: '完了',
            transactionId: '2345639',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/27 23:54:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1234ccc',
        },
        {
            date: '2021/6/25 13:54:56',
            transactionType: '付与取消',
            transactionStatus: '完了',
            transactionId: '3456740',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1d2d3d4d',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: '決済',
            transactionStatus: '完了',
            transactionId: '4567841',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678905555',
            amount: '1,000',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/29 23:59:59',
            company: 'オリエンタルランド株式会社',
            store: '浦安店',
            terminalType: 'マルチ決済端末',
            terminalId: 'aaaaa09826482',
        },
        {
            date: '2021/6/27 12:34:56',
            transactionType: '決済取消',
            transactionStatus: '完了',
            transactionId: '5678942',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678906666',
            amount: '1,500',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社フレーベル館',
            store: '北千住店',
            terminalType: 'マルチ決済機',
            terminalId: 'hsga1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ',
            transactionStatus: '完了',
            transactionId: '12345643',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678901111',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/27 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '南青山店',
            terminalType: 'チャージ機',
            terminalId: 'a1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ取消',
            transactionStatus: '完了',
            transactionId: '67890144',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678902222',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/26 23:59:54',
            company: '株式会社ポッカクリエイト',
            store: '松戸店',
            terminalType: 'POS',
            terminalId: 'bbbb1234',
        },
        {
            date: '2021/6/25 13:36:56',
            transactionType: '付与',
            transactionStatus: '完了',
            transactionId: '23456745',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/27 23:54:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1234ccc',
        },
        {
            date: '2021/6/25 13:54:56',
            transactionType: '付与取消',
            transactionStatus: '完了',
            transactionId: '3456746',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1d2d3d4d',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: '決済',
            transactionStatus: '完了',
            transactionId: '4567847',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678905555',
            amount: '1,000',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/29 23:59:59',
            company: 'オリエンタルランド株式会社',
            store: '浦安店',
            terminalType: 'マルチ決済端末',
            terminalId: 'aaaaa09826482',
        },
        {
            date: '2021/6/27 12:34:56',
            transactionType: '決済取消',
            transactionStatus: '完了',
            transactionId: '5678948',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678906666',
            amount: '1,500',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社フレーベル館',
            store: '北千住店',
            terminalType: 'マルチ決済機',
            terminalId: 'hsga1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ',
            transactionStatus: '完了',
            transactionId: '1234549',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678901111',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/27 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '南青山店',
            terminalType: 'チャージ機',
            terminalId: 'a1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ取消',
            transactionStatus: '完了',
            transactionId: '6789050',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678902222',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/26 23:59:54',
            company: '株式会社ポッカクリエイト',
            store: '松戸店',
            terminalType: 'POS',
            terminalId: 'bbbb1234',
        },
        {
            date: '2021/6/25 13:36:56',
            transactionType: '付与',
            transactionStatus: '完了',
            transactionId: '2345651',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/27 23:54:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1234ccc',
        },
        {
            date: '2021/6/25 13:54:56',
            transactionType: '付与取消',
            transactionStatus: '完了',
            transactionId: '3456752',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1d2d3d4d',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: '決済',
            transactionStatus: '完了',
            transactionId: '4567853',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678905555',
            amount: '1,000',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/29 23:59:59',
            company: 'オリエンタルランド株式会社',
            store: '浦安店',
            terminalType: 'マルチ決済端末',
            terminalId: 'aaaaa09826482',
        },
        {
            date: '2021/6/27 12:34:56',
            transactionType: '決済取消',
            transactionStatus: '完了',
            transactionId: '5678954',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678906666',
            amount: '1,500',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社フレーベル館',
            store: '北千住店',
            terminalType: 'マルチ決済機',
            terminalId: 'hsga1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ',
            transactionStatus: '完了',
            transactionId: '12345655',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678901111',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/27 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '南青山店',
            terminalType: 'チャージ機',
            terminalId: 'a1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ取消',
            transactionStatus: '完了',
            transactionId: '67890156',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678902222',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/26 23:59:54',
            company: '株式会社ポッカクリエイト',
            store: '松戸店',
            terminalType: 'POS',
            terminalId: 'bbbb1234',
        },
        {
            date: '2021/6/25 13:36:56',
            transactionType: '付与',
            transactionStatus: '完了',
            transactionId: '23456757',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/27 23:54:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1234ccc',
        },
        {
            date: '2021/6/25 13:54:56',
            transactionType: '付与取消',
            transactionStatus: '完了',
            transactionId: '3456758',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1d2d3d4d',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: '決済',
            transactionStatus: '完了',
            transactionId: '4567859',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678905555',
            amount: '1,000',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/29 23:59:59',
            company: 'オリエンタルランド株式会社',
            store: '浦安店',
            terminalType: 'マルチ決済端末',
            terminalId: 'aaaaa09826482',
        },
        {
            date: '2021/6/27 12:34:56',
            transactionType: '決済取消',
            transactionStatus: '完了',
            transactionId: '5678960',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678906666',
            amount: '1,500',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社フレーベル館',
            store: '北千住店',
            terminalType: 'マルチ決済機',
            terminalId: 'hsga1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ',
            transactionStatus: '完了',
            transactionId: '1234561',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678901111',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/27 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '南青山店',
            terminalType: 'チャージ機',
            terminalId: 'a1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ取消',
            transactionStatus: '完了',
            transactionId: '6789062',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678902222',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/26 23:59:54',
            company: '株式会社ポッカクリエイト',
            store: '松戸店',
            terminalType: 'POS',
            terminalId: 'bbbb1234',
        },
        {
            date: '2021/6/25 13:36:56',
            transactionType: '付与',
            transactionStatus: '完了',
            transactionId: '2345663',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/27 23:54:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1234ccc',
        },
        {
            date: '2021/6/25 13:54:56',
            transactionType: '付与取消',
            transactionStatus: '完了',
            transactionId: '3456764',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1d2d3d4d',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: '決済',
            transactionStatus: '完了',
            transactionId: '4567865',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678905555',
            amount: '1,000',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/29 23:59:59',
            company: 'オリエンタルランド株式会社',
            store: '浦安店',
            terminalType: 'マルチ決済端末',
            terminalId: 'aaaaa09826482',
        },
        {
            date: '2021/6/27 12:34:56',
            transactionType: '決済取消',
            transactionStatus: '完了',
            transactionId: '5678966',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678906666',
            amount: '1,500',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社フレーベル館',
            store: '北千住店',
            terminalType: 'マルチ決済機',
            terminalId: 'hsga1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ',
            transactionStatus: '完了',
            transactionId: '12345667',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678901111',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/27 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '南青山店',
            terminalType: 'チャージ機',
            terminalId: 'a1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ取消',
            transactionStatus: '完了',
            transactionId: '67890168',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678902222',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/26 23:59:54',
            company: '株式会社ポッカクリエイト',
            store: '松戸店',
            terminalType: 'POS',
            terminalId: 'bbbb1234',
        },
        {
            date: '2021/6/25 13:36:56',
            transactionType: '付与',
            transactionStatus: '完了',
            transactionId: '23456769',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/27 23:54:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1234ccc',
        },
        {
            date: '2021/6/25 13:54:56',
            transactionType: '付与取消',
            transactionStatus: '完了',
            transactionId: '3456770',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1d2d3d4d',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: '決済',
            transactionStatus: '完了',
            transactionId: '4567871',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678905555',
            amount: '1,000',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/29 23:59:59',
            company: 'オリエンタルランド株式会社',
            store: '浦安店',
            terminalType: 'マルチ決済端末',
            terminalId: 'aaaaa09826482',
        },
        {
            date: '2021/6/27 12:34:56',
            transactionType: '決済取消',
            transactionStatus: '完了',
            transactionId: '5678972',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678906666',
            amount: '1,500',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社フレーベル館',
            store: '北千住店',
            terminalType: 'マルチ決済機',
            terminalId: 'hsga1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ',
            transactionStatus: '完了',
            transactionId: '1234573',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678901111',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/27 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '南青山店',
            terminalType: 'チャージ機',
            terminalId: 'a1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ取消',
            transactionStatus: '完了',
            transactionId: '6789074',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678902222',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/26 23:59:54',
            company: '株式会社ポッカクリエイト',
            store: '松戸店',
            terminalType: 'POS',
            terminalId: 'bbbb1234',
        },
        {
            date: '2021/6/25 13:36:56',
            transactionType: '付与',
            transactionStatus: '完了',
            transactionId: '2345675',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/27 23:54:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1234ccc',
        },
        {
            date: '2021/6/25 13:54:56',
            transactionType: '付与取消',
            transactionStatus: '完了',
            transactionId: '3456776',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1d2d3d4d',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: '決済',
            transactionStatus: '完了',
            transactionId: '4567877',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678905555',
            amount: '1,000',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/29 23:59:59',
            company: 'オリエンタルランド株式会社',
            store: '浦安店',
            terminalType: 'マルチ決済端末',
            terminalId: 'aaaaa09826482',
        },
        {
            date: '2021/6/27 12:34:56',
            transactionType: '決済取消',
            transactionStatus: '完了',
            transactionId: '5678978',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678906666',
            amount: '1,500',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社フレーベル館',
            store: '北千住店',
            terminalType: 'マルチ決済機',
            terminalId: 'hsga1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ',
            transactionStatus: '完了',
            transactionId: '12345679',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678901111',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/27 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '南青山店',
            terminalType: 'チャージ機',
            terminalId: 'a1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ取消',
            transactionStatus: '完了',
            transactionId: '67890180',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678902222',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/26 23:59:54',
            company: '株式会社ポッカクリエイト',
            store: '松戸店',
            terminalType: 'POS',
            terminalId: 'bbbb1234',
        },
        {
            date: '2021/6/25 13:36:56',
            transactionType: '付与',
            transactionStatus: '完了',
            transactionId: '23456781',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/27 23:54:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1234ccc',
        },
        {
            date: '2021/6/25 13:54:56',
            transactionType: '付与取消',
            transactionStatus: '完了',
            transactionId: '3456782',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1d2d3d4d',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: '決済',
            transactionStatus: '完了',
            transactionId: '4567883',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678905555',
            amount: '1,000',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/29 23:59:59',
            company: 'オリエンタルランド株式会社',
            store: '浦安店',
            terminalType: 'マルチ決済端末',
            terminalId: 'aaaaa09826482',
        },
        {
            date: '2021/6/27 12:34:56',
            transactionType: '決済取消',
            transactionStatus: '完了',
            transactionId: '5678984',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678906666',
            amount: '1,500',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社フレーベル館',
            store: '北千住店',
            terminalType: 'マルチ決済機',
            terminalId: 'hsga1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ',
            transactionStatus: '完了',
            transactionId: '1234585',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678901111',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/27 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '南青山店',
            terminalType: 'チャージ機',
            terminalId: 'a1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ取消',
            transactionStatus: '完了',
            transactionId: '6789086',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678902222',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/26 23:59:54',
            company: '株式会社ポッカクリエイト',
            store: '松戸店',
            terminalType: 'POS',
            terminalId: 'bbbb1234',
        },
        {
            date: '2021/6/25 13:36:56',
            transactionType: '付与',
            transactionStatus: '完了',
            transactionId: '2345687',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/27 23:54:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1234ccc',
        },
        {
            date: '2021/6/25 13:54:56',
            transactionType: '付与取消',
            transactionStatus: '完了',
            transactionId: '3456788',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1d2d3d4d',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: '決済',
            transactionStatus: '完了',
            transactionId: '4567889',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678905555',
            amount: '1,000',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/29 23:59:59',
            company: 'オリエンタルランド株式会社',
            store: '浦安店',
            terminalType: 'マルチ決済端末',
            terminalId: 'aaaaa09826482',
        },
        {
            date: '2021/6/27 12:34:56',
            transactionType: '決済取消',
            transactionStatus: '完了',
            transactionId: '5678990',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678906666',
            amount: '1,500',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社フレーベル館',
            store: '北千住店',
            terminalType: 'マルチ決済機',
            terminalId: 'hsga1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ',
            transactionStatus: '完了',
            transactionId: '12345691',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678901111',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/27 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '南青山店',
            terminalType: 'チャージ機',
            terminalId: 'a1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: 'チャージ取消',
            transactionStatus: '完了',
            transactionId: '67890192',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678902222',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            grantDate: '2021/6/26 23:59:54',
            company: '株式会社ポッカクリエイト',
            store: '松戸店',
            terminalType: 'POS',
            terminalId: 'bbbb1234',
        },
        {
            date: '2021/6/25 13:36:56',
            transactionType: '付与',
            transactionStatus: '完了',
            transactionId: '23456793',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/27 23:54:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1234ccc',
        },
        {
            date: '2021/6/25 13:54:56',
            transactionType: '付与取消',
            transactionStatus: '完了',
            transactionId: '3456794',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            terminalType: 'POS',
            terminalId: '1d2d3d4d',
        },
        {
            date: '2021/6/25 12:34:56',
            transactionType: '決済',
            transactionStatus: '完了',
            transactionId: '4567895',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678905555',
            amount: '1,000',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/29 23:59:59',
            company: 'オリエンタルランド株式会社',
            store: '浦安店',
            terminalType: 'マルチ決済端末',
            terminalId: 'aaaaa09826482',
        },
        {
            date: '2021/6/27 12:34:56',
            transactionType: '決済取消',
            transactionStatus: '完了',
            transactionId: '5678996',
            cardName: 'クリエカード',
            cardType: '電子マネーカード',
            cardId: '123456789012345678906666',
            amount: '1,500',
            event: '利用促進CP',
            grant: '500',
            grantDate: '2021/6/28 23:59:59',
            company: '株式会社フレーベル館',
            store: '北千住店',
            terminalType: 'マルチ決済機',
            terminalId: 'hsga1a2a3a4',
        },
    ];
    singleSelect = false;
    listPeriod = ['今日', '昨日', '前週', '先月', 'カスタム'];
    listTransactionType = [
        'チャージ',
        'チャージ取消',
        '付与',
        '付与取消',
        '決数',
        '決数取消',
        'ボーナス利用',
        'ボーナス利用取消',
        'カード付替',
    ];
    listTerminalType = [
        'チャージ',
        'チャージ取消',
        '付与',
        '付与取消',
        '決数',
        '決数取消',
        'ボーナス利用',
        'ボーナス利用取消',
        'カード付替',
    ];
    listCardStatus = [
        'アクティベート',
        '未アクティベート',
        '利用停止',
        '付替済み',
        '破棄',
    ];
    listTransactionTypeSelected = [];
    listTerminalTypeSelected = [];
    listCardStatusSelected = [];
    selected: HistoryItem[] = [];
    transactionIdSeleted: string[] = [];
    showPopupSelect = false;
    showPopupConfirm = false;
    showPopupCsvDownload = false;
    menu1 = false;
    menu2 = false;
    date1 = null;
    date2 = null;
    dateFormatted = null as string | null;
    dateFormatted2 = null as string | null;
    radios = null;
    showSnackbar = false;
    // show popup select
    popupSelect(): void {
        this.showPopupSelect = !this.showPopupSelect;
    }
    popupConfirm(): void {
        this.showPopupConfirm = true;
    }
    popupCsvDownload(): void {
        this.showPopupCsvDownload = true;
    }
    executionCsvDownload(): void {
        this.showPopupCsvDownload = false;
        this.showSnackbar = true;
    }
    public countSelected(): void {
        this.showPopupConfirm = false;
        this.showPopupSelect = false;
        // call api denide history
        // call api success
        this.selected.map((item: HistoryItem) => {
            this.transactionIdSeleted.push(item.transactionId);
        });
        this.selected = [];
    }
    public checkInTransaction(item: HistoryItem): boolean {
        return this.transactionIdSeleted.includes(item.transactionId)
            ? true
            : false;
    }

    @Watch('date1')
    onDateChanged(): void {
        this.dateFormatted = this.formatDate(this.date1);
    }
    @Watch('date2')
    onDate2Changed(): void {
        this.dateFormatted2 = this.formatDate(this.date2);
    }
    formatDate(date: string | null): string | null {
        if (!date) return null;
        const [year, month, day] = date.split('-');
        return `${year}/${month}/${day}`;
    }
}
</script>
