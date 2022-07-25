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
                    {{ $t('card.cardManagement') }}
                </v-col>
                <v-spacer></v-spacer>
                <v-col cols="auto">
                    <CsvDownload />
                </v-col>
            </v-row>
        </div>
        <v-row no-gutters align="center" style="width: 100%; min-width: 960px">
            <div class="pl-0 pr-2">
                <v-select
                    full-width
                    dense
                    :label="$t('card.cardSettingName')"
                    outlined
                    hide-details
                    multiple
                    style="width: 150px"
                ></v-select>
            </div>
            <div class="pr-0 pl-2">
                <v-select
                    v-model="cardStatusSelected"
                    full-width
                    dense
                    :label="$t('card.cardStatus')"
                    outlined
                    hide-details
                    :items="cardStatus"
                    multiple
                    style="width: 195px"
                >
                    <template v-slot:selection="{ item, index }">
                        <div
                            v-if="cardStatusSelected.length === 1"
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
                            {{ cardStatusSelected.length }}件選択
                        </span>
                    </template>
                </v-select>
            </div>
            <v-col cols="auto" class="py-0 px-4">
                <v-divider vertical style="height: 40px"></v-divider>
            </v-col>
            <div class="pa-2 pl-0">
                <v-text-field
                    :placeholder="$t('card.cardNumber')"
                    outlined
                    dense
                    hide-details
                    style="width: 195px"
                ></v-text-field>
            </div>
            <v-col class="py-0 px-2 pr-0" cols="auto" style="height: 40px">
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
            <v-col cols="auto" class="py-0 px-2 ml-3">
                <v-divider vertical style="height: 40px"></v-divider>
            </v-col>
            <v-col
                cols="auto"
                class="text-body-2 grey--text text--darken-2 text-right"
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
                    color="primary"
                ></v-radio>
                <v-radio
                    :label="$t('card.cardTest')"
                    value="radio-2"
                    color="primary"
                ></v-radio>
            </v-radio-group>
        </v-row>
        <v-divider class="mt-4 mb-6"></v-divider>
        <v-row class="mx-auto my-8" style="width: 156px">
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
                class=".table-bordered"
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
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                class="ma-3"
                                color="grey lighten-2"
                                v-bind="attrs"
                                small
                                elevation="0"
                                v-on="on"
                                @click="popupSelect"
                            >
                                {{ $t('card.cardList.cardStatusChange') }}
                            </v-btn>
                        </template>

                        <v-card>
                            <v-list>
                                <v-list-item three-line>
                                    <v-list-item-content>
                                        <v-select
                                            dense
                                            outlined
                                            :label="
                                                $t('card.cardList.cardStatus')
                                            "
                                            hide-details
                                            :items="cardStatus"
                                        ></v-select>
                                        <v-row
                                            class="
                                                mx-auto
                                                mt-4
                                                mb-0
                                                d-flex
                                                justify-end
                                            "
                                        >
                                            <v-col cols="6" class="pa-0 mr-2">
                                                <v-btn
                                                    class="pa-2"
                                                    color="grey darken-1"
                                                    height="40"
                                                    block
                                                    elevation="0"
                                                    outlined
                                                    @click="popupSelect"
                                                >
                                                    {{ $t('common.cancel') }}
                                                </v-btn>
                                            </v-col>
                                            <v-col class="pa-0 col-auto">
                                                <v-btn
                                                    color="white"
                                                    class="pa-2 primary"
                                                    height="40"
                                                    elevation="0"
                                                    right
                                                    @click="popupConfirm"
                                                >
                                                    {{ $t('common.change') }}
                                                </v-btn>
                                            </v-col>
                                        </v-row>
                                    </v-list-item-content>
                                </v-list-item>
                            </v-list>
                        </v-card>
                    </v-menu>
                    <v-divider></v-divider>
                </template>
                <template v-slot:[`footer.page-text`]="items">
                    {{ items.pageStart }} - {{ items.pageStop }} /
                    {{ items.itemsLength }}
                </template>
                <template v-slot:[`item.cardName`]="{ item }">
                    {{ item.cardName }}
                    <v-chip
                        v-if="checkInTransaction(item)"
                        class="ma-2"
                        color="primary"
                        outlined
                    >
                        {{ $t('common.cancelApprovalWaiting') }}
                        <span class="material-icons">delete</span>
                    </v-chip>
                </template>
                <template v-slot:[`item.btnDetail`]="{ item }">
                    {{ item.btnDetail }}
                    <router-link to="/cardDetail" style="text-decoration: none">
                        <v-btn
                            color="grey lighten-2"
                            class="grey darken-4--text py-4"
                            height="30"
                            block
                            elevation="0"
                            width="2px"
                            small
                        >
                            {{ $t('card.cardList.detail') }}
                        </v-btn>
                    </router-link>
                </template>
            </v-data-table>
        </v-card>
        <v-row justify="center">
            <v-dialog
                v-model="showPopupConfirm"
                max-width="580"
                :close-on-click="true"
            >
                <v-card>
                    <v-card-title class="text-h5">
                        {{ $t('card.cardList.confirmChangeStatus') }}
                        <v-spacer></v-spacer>
                        <v-btn icon @click="showPopupConfirm = false">
                            <v-icon>close</v-icon>
                        </v-btn>
                    </v-card-title>
                    <v-card-text style="color: black">
                        {{ $t('card.cardList.applyConfirmMsg') }}
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
        </v-row>
    </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import { CardItem } from '../models/CardModel';
import CsvDownload from '../components/CsvDownload.vue';
@Component({ components: { CsvDownload } })
export default class History extends Vue {
    headers = [
        {
            text: this.$t('card.cardSettingName'),
            value: 'cardName',
            sortable: false,
        },
        {
            text: this.$t('card.cardStatus'),
            value: 'cardStatus',
            sortable: false,
        },
        { text: this.$t('card.cardNumber'), value: 'cardId', sortable: false },
        {
            text: this.$t('card.cardSettingType'),
            value: 'cardType',
            sortable: false,
        },
        {
            text: this.$t('common.note'),
            value: 'comment',
            sortable: false,
        },
        { text: '', value: 'btnDetail', sortable: false },
    ];
    promotions = [
        {
            transactionId: '123456',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '678901',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '234567',
            cardName: 'クリエカード',
            cardStatus: '付け替え済み',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '345678',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: 'このカード注意！（松田）',
        },
        {
            transactionId: '456789',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '567890',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '1234567',
            cardName: 'クリエカード',
            cardStatus: '付け替え済み',
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
            comment: '',
        },
        {
            transactionId: '6789017',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '2345677',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '3456787',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '4567897',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '5678907',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '123401',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '678902',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '234503',
            cardName: 'クリエカード',
            cardStatus: '付け替え済み',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '345604',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: 'このカード注意！（松田）',
        },
        {
            transactionId: '456705',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '567806',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '1234507',
            cardName: 'クリエカード',
            cardStatus: '付け替え済み',
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
            comment: '',
        },
        {
            transactionId: '6789008',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '2345609',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '3456710',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '4567811',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '5678912',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '123413',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '678914',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '234515',
            cardName: 'クリエカード',
            cardStatus: '付け替え済み',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '345616',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: 'このカード注意！（松田）',
        },
        {
            transactionId: '456717',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '567818',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '1234519',
            cardName: 'クリエカード',
            cardStatus: '付け替え済み',
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
            comment: '',
        },
        {
            transactionId: '6789020',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '2345621',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '3456722',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '4567823',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '5678924',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '123425',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '678926',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '234527',
            cardName: 'クリエカード',
            cardStatus: '付け替え済み',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '345628',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: 'このカード注意！（松田）',
        },
        {
            transactionId: '456729',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '567830',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '1234531',
            cardName: 'クリエカード',
            cardStatus: '付け替え済み',
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
            comment: '',
        },
        {
            transactionId: '6789032',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '2345633',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '3456734',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '4567835',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '5678936',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '123437',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '678938',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '234539',
            cardName: 'クリエカード',
            cardStatus: '付け替え済み',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '345640',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: 'このカード注意！（松田）',
        },
        {
            transactionId: '456741',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '567842',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '1234543',
            cardName: 'クリエカード',
            cardStatus: '付け替え済み',
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
            comment: '',
        },
        {
            transactionId: '6789044',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '2345645',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '3456746',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '4567847',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '5678948',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '123449',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '678950',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '234551',
            cardName: 'クリエカード',
            cardStatus: '付け替え済み',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '345652',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: 'このカード注意！（松田）',
        },
        {
            transactionId: '456753',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '567854',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '1234555',
            cardName: 'クリエカード',
            cardStatus: '付け替え済み',
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
            comment: '',
        },
        {
            transactionId: '6789056',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '2345657',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '3456758',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '4567859',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '5678960',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '123461',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '678962',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '234563',
            cardName: 'クリエカード',
            cardStatus: '付け替え済み',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '345664',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: 'このカード注意！（松田）',
        },
        {
            transactionId: '456765',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '567866',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '12345678',
            cardName: 'クリエカード',
            cardStatus: '付け替え済み',
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
            comment: '',
        },
        {
            transactionId: '6789068',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '2345669',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '3456770',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '4567871',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '5678972',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '123473',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '678974',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '234575',
            cardName: 'クリエカード',
            cardStatus: '付け替え済み',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '345676',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: 'このカード注意！（松田）',
        },
        {
            transactionId: '456777',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '567878',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '1234579',
            cardName: 'クリエカード',
            cardStatus: '付け替え済み',
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
            comment: '',
        },
        {
            transactionId: '6789080',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '2345681',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '3456782',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '4567883',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '5678984',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '123485',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '678986',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '234587',
            cardName: 'クリエカード',
            cardStatus: '付け替え済み',
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
            comment: '',
            btnDetail: '',
        },
        {
            transactionId: '345688',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: 'このカード注意！（松田）',
        },
        {
            transactionId: '45678977',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '567890122',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '1234591',
            cardName: 'クリエカード',
            cardStatus: '付け替え済み',
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
            comment: '',
        },
        {
            transactionId: '6789092',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '2345693',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '3456794',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '4567895',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
        {
            transactionId: '5678996',
            cardName: 'クリエカード',
            cardStatus: 'アクティベート',
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
            comment: '',
        },
    ];
    cardStatus = [
        'アクティベート',
        '未アクティベート',
        '利用停止',
        '付替済み',
        '破棄',
    ];
    cardStatusSelected = [];
    singleSelect = false;
    selected: CardItem[] = [];
    transactionIdSeleted: string[] = [];
    showPopupSelect = false;
    showPopupConfirm = false;
    radios = null;
    // show popup select
    popupSelect(): void {
        this.showPopupSelect = !this.showPopupSelect;
    }
    popupConfirm(): void {
        this.showPopupConfirm = true;
    }
    countSelected(): void {
        this.showPopupConfirm = false;
        this.showPopupSelect = false;
        // call api denide history
        // call api success
        this.selected.map((item: CardItem) => {
            this.transactionIdSeleted.push(item.transactionId);
        });
        this.selected = [];
    }
    checkInTransaction(item: CardItem): boolean {
        return this.transactionIdSeleted.includes(item.transactionId)
            ? true
            : false;
    }
}
</script>
