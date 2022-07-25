<template>
    <v-container fluid class="px-8">
        <v-col
            cols="auto"
            class="
                d-flex
                flex-row
                align-center
                text-h4
                font-weight-bold
                mt-2
                mb-4
            "
        >
            {{ $t('transaction.cancelApprove.approvalDecision') }} /
            {{ $t('transaction.cancelApprove.transactionHistoryCancel') }}
        </v-col>
        <v-card outlined>
            <v-data-table
                :headers="headers"
                :items="promotions"
                :items-per-page="10"
                :footer-props="{
                    'items-per-page-options': [10, 20, 30, 50, 100],
                    'items-per-page-text': this.$t('common.itemsPerPageText'),
                }"
                :options="options"
                item-key="transaction-id"
                style="white-space: nowrap"
            >
                <template v-slot:top></template>
                <template v-slot:[`footer.page-text`]="items">
                    {{ items.pageStart }} - {{ items.pageStop }} /
                    {{ items.itemsLength }}
                </template>
            </v-data-table>
        </v-card>
        <v-row class="mx-auto my-8" style="width: 156px">
            <v-col class="pa-0 mr-1">
                <!-- Fullscreen Deny Popup -->
                <v-dialog
                    v-model="fullscreenDenyPopup"
                    fullscreen
                    hide-overlay
                    transition="dialog-bottom-transition"
                >
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            class="pa-2"
                            color="grey darken-1"
                            height="40"
                            block
                            elevation="0"
                            outlined
                            v-bind="attrs"
                            v-on="on"
                        >
                            {{ $t('common.deny') }}
                        </v-btn>
                    </template>
                    <v-card>
                        <v-toolbar
                            dark
                            flat
                            height="56"
                            dense
                            color="grey darken-3"
                        >
                            <v-btn
                                icon
                                dark
                                @click="fullscreenDenyPopup = false"
                            >
                                <v-icon>close</v-icon>
                            </v-btn>
                            <v-toolbar-title>
                                {{
                                    $t(
                                        'transaction.cancelApprove.denialReasonPopup'
                                    )
                                }}
                            </v-toolbar-title>
                            <v-spacer></v-spacer>
                            <!-- Deny Confirm Popup -->
                            <v-dialog v-model="denyConfirmPopup" width="580">
                                <template v-slot:activator="{ on, attrs }">
                                    <v-btn
                                        color="primary"
                                        v-bind="attrs"
                                        v-on="on"
                                    >
                                        {{ $t('common.apply') }}
                                    </v-btn>
                                </template>

                                <v-card>
                                    <v-card-title class="text-h6 pa-4">
                                        {{
                                            $t(
                                                'transaction.cancelApprove.denialReason.denialConfirm'
                                            )
                                        }}
                                        <v-spacer></v-spacer>
                                        <v-btn
                                            icon
                                            @click="denyConfirmPopup = false"
                                        >
                                            <v-icon>close</v-icon>
                                        </v-btn>
                                    </v-card-title>
                                    <v-card-text class="px-4 py-0">
                                        {{
                                            $t(
                                                'transaction.cancelApprove.denialReason.denialConfirmMsg'
                                            )
                                        }}
                                    </v-card-text>

                                    <v-card-actions class="pa-4">
                                        <v-spacer></v-spacer>
                                        <v-btn
                                            class="text--secondary"
                                            outlined
                                            @click="denyConfirmPopup = false"
                                        >
                                            {{ $t('common.cancel') }}
                                        </v-btn>
                                        <v-btn
                                            color="primary"
                                            elevation="0"
                                            @click="denyConfirmPopup = false"
                                        >
                                            OK
                                        </v-btn>
                                    </v-card-actions>
                                </v-card>
                            </v-dialog>
                        </v-toolbar>
                        <!-- Fullscreen Deny Popup Content -->
                        <v-container>
                            <v-col cols="8" class="mx-auto">
                                <v-col class="text-body-1">
                                    {{
                                        $t(
                                            'transaction.cancelApprove.denialReason.denialReasonMsg'
                                        )
                                    }}
                                </v-col>
                                <v-col>
                                    <v-select
                                        dense
                                        :items="denyReasonsSelectList"
                                        label="2021/6/25 12:34:56の取引"
                                        outlined
                                        hide-details
                                    ></v-select>
                                </v-col>
                                <v-col>
                                    <v-text-field
                                        class=""
                                        :label="
                                            $t(
                                                'transaction.cancelApprove.denialReason.otherReason'
                                            )
                                        "
                                        outlined
                                        hide-details
                                    ></v-text-field>
                                </v-col>
                                <v-col class="pa-3">
                                    <v-divider></v-divider>
                                </v-col>
                                <v-col>
                                    <v-select
                                        dense
                                        :items="denyReasonsSelectList"
                                        label="2021/6/25 12:34:56の取引"
                                        outlined
                                        hide-details
                                    ></v-select>
                                </v-col>
                                <v-col>
                                    <v-text-field
                                        :label="
                                            $t(
                                                'transaction.cancelApprove.denialReason.otherReason'
                                            )
                                        "
                                        outlined
                                        hide-details
                                    ></v-text-field>
                                </v-col>
                            </v-col>
                        </v-container>
                    </v-card>
                </v-dialog>
            </v-col>
            <v-col class="pa-0 ml-1">
                <!-- Approve Popup -->
                <v-dialog v-model="approvePopup" width="580">
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            color="white"
                            class="pa-2 primary"
                            height="40"
                            block
                            elevation="0"
                            v-bind="attrs"
                            v-on="on"
                        >
                            {{ $t('common.approve') }}
                        </v-btn>
                    </template>

                    <v-card>
                        <v-card-title class="text-h6 pa-4">
                            {{
                                $t('transaction.cancelApprove.approvalConfirm')
                            }}
                            <v-spacer></v-spacer>
                            <v-btn icon @click="approvePopup = false">
                                <v-icon>close</v-icon>
                            </v-btn>
                        </v-card-title>
                        <v-card-text class="px-4 py-0">
                            {{
                                $t(
                                    'transaction.cancelApprove.approvalConfirmMsg'
                                )
                            }}
                        </v-card-text>

                        <v-card-actions class="pa-4">
                            <v-spacer></v-spacer>
                            <v-btn
                                class="text--secondary"
                                outlined
                                @click="approvePopup = false"
                            >
                                {{ $t('common.cancel') }}
                            </v-btn>
                            <v-btn
                                color="primary"
                                elevation="0"
                                @click="approvePopup = false"
                            >
                                OK
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </v-col>
        </v-row>
    </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';

@Component
export default class History extends Vue {
    fullscreenDenyPopup = false;
    denyConfirmPopup = false;
    approvePopup = false;
    options = null;
    denyReasonsSelectList = [
        this.$t('transaction.cancelApprove.denialReason.select.doubleCheck'),
        this.$t('transaction.cancelApprove.denialReason.select.cannotApprove'),
        this.$t('common.others'),
    ];
    headers = [
        {
            text: this.$t('transaction.transactionDateTime'),
            align: 'start',
            value: 'date',
            sortable: false,
        },
        {
            text: this.$t('transaction.transactionType'),
            value: 'transaction-type',
            sortable: false,
        },
        {
            text: this.$t('transaction.transactionStatus'),
            value: 'transaction-status',
            sortable: false,
        },
        {
            text: this.$t('transaction.transactionNumber'),
            value: 'transaction-id',
            sortable: false,
        },
        {
            text: this.$t('card.cardSettingName'),
            value: 'card-name',
            sortable: false,
        },
        {
            text: this.$t('card.cardSettingType'),
            value: 'card-type',
            sortable: false,
        },
        { text: this.$t('card.cardNumber'), value: 'card-id', sortable: false },
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
            value: 'grant-date',
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
            value: 'terminal-type',
            sortable: false,
        },
        {
            text: this.$t('transaction.history.terminalNumber'),
            value: 'terminal-id',
            sortable: false,
        },
    ];
    promotions = [
        {
            date: '2021/6/25 12:34:56',
            'transaction-type': 'チャージ',
            'transaction-status': '完了',
            'transaction-id': '123456',
            'card-name': 'クリエカード',
            'card-type': '電子マネーカード',
            'card-id': '123456789012345678901111',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            'grant-date': '2021/6/27 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '南青山店',
            'terminal-type': 'チャージ機',
            'terminal-id': 'a1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            'transaction-type': 'チャージ取消',
            'transaction-status': '完了',
            'transaction-id': '678901',
            'card-name': 'クリエカード',
            'card-type': '電子マネーカード',
            'card-id': '123456789012345678902222',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            'grant-date': '2021/6/26 23:59:54',
            company: '株式会社ポッカクリエイト',
            store: '松戸店',
            'terminal-type': 'POS',
            'terminal-id': 'bbbb1234',
        },
        {
            date: '2021/6/25 13:36:56',
            'transaction-type': '付与',
            'transaction-status': '完了',
            'transaction-id': '234567',
            'card-name': 'クリエカード',
            'card-type': '電子マネーカード',
            'card-id': '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            'grant-date': '2021/6/27 23:54:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            'terminal-type': 'POS',
            'terminal-id': '1234ccc',
        },
        {
            date: '2021/6/25 13:54:56',
            'transaction-type': '付与取消',
            'transaction-status': '完了',
            'transaction-id': '345678',
            'card-name': 'クリエカード',
            'card-type': '電子マネーカード',
            'card-id': '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            'grant-date': '2021/6/28 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            'terminal-type': 'POS',
            'terminal-id': '1d2d3d4d',
        },
        {
            date: '2021/6/25 12:34:56',
            'transaction-type': '決済',
            'transaction-status': '完了',
            'transaction-id': '456789',
            'card-name': 'クリエカード',
            'card-type': '電子マネーカード',
            'card-id': '123456789012345678905555',
            amount: '1,000',
            event: '利用促進CP',
            grant: '500',
            'grant-date': '2021/6/29 23:59:59',
            company: 'オリエンタルランド株式会社',
            store: '浦安店',
            'terminal-type': 'マルチ決済端末',
            'terminal-id': 'aaaaa09826482',
        },
        {
            date: '2021/6/27 12:34:56',
            'transaction-type': '決済取消',
            'transaction-status': '完了',
            'transaction-id': '567890',
            'card-name': 'クリエカード',
            'card-type': '電子マネーカード',
            'card-id': '123456789012345678906666',
            amount: '1,500',
            event: '利用促進CP',
            grant: '500',
            'grant-date': '2021/6/28 23:59:59',
            company: '株式会社フレーベル館',
            store: '北千住店',
            'terminal-type': 'マルチ決済機',
            'terminal-id': 'hsga1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            'transaction-type': 'チャージ',
            'transaction-status': '完了',
            'transaction-id': '1234567',
            'card-name': 'クリエカード',
            'card-type': '電子マネーカード',
            'card-id': '123456789012345678901111',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            'grant-date': '2021/6/27 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '南青山店',
            'terminal-type': 'チャージ機',
            'terminal-id': 'a1a2a3a4',
        },
        {
            date: '2021/6/25 12:34:56',
            'transaction-type': 'チャージ取消',
            'transaction-status': '完了',
            'transaction-id': '6789017',
            'card-name': 'クリエカード',
            'card-type': '電子マネーカード',
            'card-id': '123456789012345678902222',
            amount: '2,000',
            event: 'チャージアップCP',
            grant: '200',
            'grant-date': '2021/6/26 23:59:54',
            company: '株式会社ポッカクリエイト',
            store: '松戸店',
            'terminal-type': 'POS',
            'terminal-id': 'bbbb1234',
        },
        {
            date: '2021/6/25 13:36:56',
            'transaction-type': '付与',
            'transaction-status': '完了',
            'transaction-id': '2345677',
            'card-name': 'クリエカード',
            'card-type': '電子マネーカード',
            'card-id': '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            'grant-date': '2021/6/27 23:54:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            'terminal-type': 'POS',
            'terminal-id': '1234ccc',
        },
        {
            date: '2021/6/25 13:54:56',
            'transaction-type': '付与取消',
            'transaction-status': '完了',
            'transaction-id': '3456787',
            'card-name': 'クリエカード',
            'card-type': '電子マネーカード',
            'card-id': '123456789012345678903333',
            amount: '500',
            event: '雨の日CP',
            grant: '50',
            'grant-date': '2021/6/28 23:59:59',
            company: '株式会社ポッカクリエイト',
            store: '本部',
            'terminal-type': 'POS',
            'terminal-id': '1d2d3d4d',
        },
        {
            date: '2021/6/25 12:34:56',
            'transaction-type': '決済',
            'transaction-status': '完了',
            'transaction-id': '4567897',
            'card-name': 'クリエカード',
            'card-type': '電子マネーカード',
            'card-id': '123456789012345678905555',
            amount: '1,000',
            event: '利用促進CP',
            grant: '500',
            'grant-date': '2021/6/29 23:59:59',
            company: 'オリエンタルランド株式会社',
            store: '浦安店',
            'terminal-type': 'マルチ決済端末',
            'terminal-id': 'aaaaa09826482',
        },
        {
            date: '2021/6/27 12:34:56',
            'transaction-type': '決済取消',
            'transaction-status': '完了',
            'transaction-id': '5678907',
            'card-name': 'クリエカード',
            'card-type': '電子マネーカード',
            'card-id': '123456789012345678906666',
            amount: '1,500',
            event: '利用促進CP',
            grant: '500',
            'grant-date': '2021/6/28 23:59:59',
            company: '株式会社フレーベル館',
            store: '北千住店',
            'terminal-type': 'マルチ決済機',
            'terminal-id': 'hsga1a2a3a4',
        },
    ];
}
</script>
