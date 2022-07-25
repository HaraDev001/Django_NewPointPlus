<template>
    <v-container fluid class="pa-0">
        <v-divider class="mb-5"></v-divider>
        <v-row class="pa-0 pl-3" align="center" style="width: 880px">
            <v-col class="pa-0 pr-2">
                <v-select
                    dense
                    :label="$t('transaction.aggregationPeriod')"
                    outlined
                    hide-details
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
                            v-bind="attrs"
                            class="select-datepicker"
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
                            v-bind="attrs"
                            class="select-datepicker"
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
                class="
                    text-body-2
                    grey--text
                    text--darken-2 text-right
                    py-0
                    px-2
                "
            >
                {{ $t('card.cardDisplayType') }}：
            </v-col>
            <v-radio-group row mandatory class="font-weight-bold">
                <v-radio
                    :label="$t('card.cardProduction')"
                    value="radio-1"
                ></v-radio>
                <v-radio :label="$t('card.cardTest')" value="radio-2"></v-radio>
            </v-radio-group>
        </v-row>
        <v-divider class="my-6"></v-divider>
        <v-row class="pl-3 pb-2 py-0" align="center" style="width: 1047px">
            <v-col class="px-2 pl-0">
                <v-select
                    dense
                    :label="$t('transaction.statistic.aggregationCriteria')"
                    outlined
                    hide-details
                ></v-select>
            </v-col>
            <span class="material-icons">east</span>
            <v-col class="py-0 px-2">
                <v-select
                    dense
                    :label="$t('card.cardSettingName')"
                    outlined
                    hide-details
                ></v-select>
            </v-col>

            <v-col class="py-0 px-2">
                <v-select
                    dense
                    :label="$t('transaction.statistic.managementTag')"
                    outlined
                    hide-details
                ></v-select>
            </v-col>
            <v-col class="py-0 px-2">
                <v-select
                    dense
                    :label="$t('transaction.statistic.enterprise')"
                    outlined
                    hide-details
                ></v-select>
            </v-col>

            <v-col class="py-0 px-2">
                <v-select
                    dense
                    :label="$t('transaction.statistic.store')"
                    outlined
                    hide-details
                ></v-select>
            </v-col>
            <v-col class="py-0 px-2">
                <v-select
                    dense
                    :label="$t('transaction.statistic.storeTerminal')"
                    outlined
                    hide-details
                ></v-select>
            </v-col>
        </v-row>
        <v-divider class="mt-4 mb-6"></v-divider>
        <v-row class="mx-auto my-2" style="width: 156px">
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
                :headers="showHeaders"
                :items="promotions"
                :items-per-page="10"
                :footer-props="{
                    'items-per-page-options': [10, 20, 30, 50, 100],
                    'items-per-page-text': this.$t('common.itemsPerPageText'),
                }"
                item-key="key3"
                style="white-space: nowrap"
                hide-default-header
                class="transition-table"
                :item-class="itemRowBackground"
            >
                <template v-slot:top>
                    <v-toolbar flat>
                        <template v-if="editItem">
                            <v-toolbar-title>
                                {{ $t('transaction.statistic.itemToHide') }}
                            </v-toolbar-title>
                            <span class="material-icons px-3">visibility</span>
                            <v-toolbar-title>
                                {{ $t('transaction.statistic.clickTheItem') }}
                            </v-toolbar-title>
                        </template>
                        <template v-else>
                            <v-toolbar-title class="pr-3">
                                {{
                                    $t(
                                        'transaction.statistic.transactionTotalCard'
                                    )
                                }}
                            </v-toolbar-title>
                            <v-toolbar-title>
                                {{
                                    $t(
                                        'transaction.statistic.aggregationCriteriaDaily'
                                    )
                                }}
                            </v-toolbar-title>
                        </template>
                        <v-spacer></v-spacer>
                        <v-btn
                            :color="editItem ? 'primary' : ''"
                            class="my-2 py-1 edit-item"
                            outlined
                            @click="changeTransactionState"
                        >
                            <span class="material-icons pr-2">visibility</span>
                            <span v-if="editItem">
                                {{ $t('transaction.statistic.editItemDone') }}
                            </span>
                            <span v-else>
                                {{ $t('transaction.statistic.editItem') }}
                            </span>
                        </v-btn>
                    </v-toolbar>
                    <v-divider></v-divider>
                </template>
                <template v-slot:header="{ props: { headers } }">
                    <thead
                        :class="editItem ? 'white--text orange darken-3' : ''"
                    >
                        <tr>
                            <template>
                                <th
                                    v-for="(item, i) in headers"
                                    :key="item.value"
                                    class="text-right"
                                    :class="{
                                        transactionSelected: condition.includes(
                                            item.value
                                        ),
                                    }"
                                >
                                    <div
                                        v-if="i != 0"
                                        class="
                                            d-flex
                                            flex-row-reverse
                                            align-center
                                        "
                                        :class="editItem ? 'white-text' : ''"
                                    >
                                        <v-checkbox
                                            v-if="editItem"
                                            v-model="transactionSelected"
                                            :value="item.value"
                                            hide-details
                                            class="mt-0 pl-3 pt-0 mr-n3"
                                            :on-icon="'visibility_off'"
                                            :off-icon="'remove_red_eye'"
                                            color="grey darken-1"
                                            @click="selectColumn(item.value)"
                                        ></v-checkbox>
                                        <span>
                                            {{ item.text }}
                                        </span>
                                    </div>
                                </th>
                            </template>
                        </tr>
                    </thead>
                </template>
                <template v-slot:[`footer.page-text`]="items">
                    {{ items.pageStart }} - {{ items.pageStop }} /
                    {{ items.itemsLength }}
                </template>
            </v-data-table>
        </v-card>
    </v-container>
</template>

<script lang="ts">
import { Vue, Component, Watch } from 'vue-property-decorator';
import { TransactionHeader } from '../models/TransactionModel';

@Component
export default class History extends Vue {
    condition: string[] = [];
    activeColumnHeader = false;
    editItem = false;
    transactionSelected: string[] = [];
    headers: TransactionHeader[] = [];

    menu1 = false;
    menu2 = false;
    date1 = null;
    date2 = null;
    dateFormatted = null as string | null;
    dateFormatted2 = null as string | null;

    headersMap: TransactionHeader[] = [
        {
            text: '',
            align: 'start',
            value: 'date',
            sortable: false,
        },
        {
            text: this.$tc('transaction.statistic.table.prepaidValue'),
            value: 'transactionType',
            sortable: false,
            align: 'right',
        },
        {
            text: this.$tc('transaction.statistic.table.number'),
            value: 'transactionStatus',
            sortable: false,
            align: 'right',
        },
        {
            text: this.$tc('transaction.statistic.table.prepaidValueCancel'),
            value: 'transactionId',
            sortable: false,
            align: 'right',
        },
        {
            text: this.$tc('transaction.statistic.table.number'),
            value: 'cardType',
            sortable: false,
            align: 'right',
        },
        {
            text: this.$tc('transaction.statistic.table.prepaidValueAmount'),
            value: 'cardName',
            sortable: false,
            align: 'right',
        },
        {
            text: this.$tc('transaction.statistic.table.numberBonuses'),
            value: 'cardId',
            sortable: false,
            align: 'right',
        },
        {
            text: this.$tc('transaction.statistic.table.prepaidValue'),
            value: 'amount',
            sortable: false,
            align: 'right',
        },
        {
            text: this.$tc('transaction.statistic.table.number'),
            value: 'event',
            sortable: false,
            align: 'right',
        },
        {
            text: this.$tc('transaction.statistic.table.prepaidValueCancel'),
            value: 'grant',
            sortable: false,
            align: 'right',
        },
        {
            text: this.$tc('transaction.statistic.table.number'),
            value: 'grantDate',
            sortable: false,
            align: 'right',
        },
        {
            text: this.$tc('transaction.statistic.table.prepaidValueAmount'),
            value: 'company',
            sortable: false,
            align: 'right',
        },
        {
            text: this.$tc('transaction.statistic.table.numberBonuses'),
            value: 'store',
            sortable: false,
            align: 'right',
        },
        {
            text: this.$tc('transaction.statistic.table.prepaidValue'),
            value: 'terminalType',
            sortable: false,
            align: 'right',
        },
        {
            text: this.$tc('transaction.statistic.table.number'),
            value: 'terminalId',
            sortable: false,
            align: 'right',
        },
    ];
    promotions = [
        {
            date: '合計',
            transactionType: '200',
            transactionStatus: '10',
            transactionId: '200',
            cardName: '10',
            cardType: '206',
            cardId: '2,050',
            amount: '2,000',
            event: '400',
            grant: '200',
            grantDate: '300',
            company: '600',
            store: '500',
            terminalType: '10',
            terminalId: '20',
        },
        {
            date: '2021/06/25',
            transactionType: '200',
            transactionStatus: '10',
            transactionId: '200',
            cardName: '10',
            cardType: '206',
            cardId: '2,050',
            amount: '2,000',
            event: '400',
            grant: '200',
            grantDate: '300',
            company: '600',
            store: '500',
            terminalType: '10',
            terminalId: '20',
        },
        {
            date: '2021/06/25',
            transactionType: '200',
            transactionStatus: '10',
            transactionId: '200',
            cardName: '10',
            cardType: '206',
            cardId: '2,050',
            amount: '2,000',
            event: '400',
            grant: '200',
            grantDate: '300',
            company: '600',
            store: '500',
            terminalType: '10',
            terminalId: '20',
        },
        {
            date: '2021/06/25',
            transactionType: '200',
            transactionStatus: '10',
            transactionId: '200',
            cardName: '10',
            cardType: '206',
            cardId: '2,050',
            amount: '2,000',
            event: '400',
            grant: '200',
            grantDate: '300',
            company: '600',
            store: '500',
            terminalType: '10',
            terminalId: '20',
        },
        {
            date: '2021/06/26',
            transactionType: '200',
            transactionStatus: '10',
            transactionId: '200',
            cardName: '10',
            cardType: '206',
            cardId: '2,050',
            amount: '2,000',
            event: '400',
            grant: '200',
            grantDate: '300',
            company: '600',
            store: '500',
            terminalType: '10',
            terminalId: '20',
        },
        {
            date: '2021/06/28',
            transactionType: '200',
            transactionStatus: '10',
            transactionId: '200',
            cardName: '10',
            cardType: '206',
            cardId: '2,050',
            amount: '2,000',
            event: '400',
            grant: '200',
            grantDate: '300',
            company: '600',
            store: '500',
            terminalType: '10',
            terminalId: '20',
        },
        {
            date: '2021/07/27',
            transactionType: '200',
            transactionStatus: '10',
            transactionId: '200',
            cardName: '10',
            cardType: '206',
            cardId: '2,050',
            amount: '2,000',
            event: '400',
            grant: '200',
            grantDate: '300',
            company: '600',
            store: '500',
            terminalType: '10',
            terminalId: '20',
        },
    ];

    // computed
    get showHeaders(): TransactionHeader[] {
        return this.headers.filter((s: TransactionHeader) =>
            this.headers.includes(s)
        );
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

    created(): void {
        this.headers = Object.values(this.headersMap);
    }

    selectColumn(i: string | null): void {
        if (i != null) {
            if (this.transactionSelected.includes(i)) {
                this.condition.push(i);
            } else {
                const index = this.condition.indexOf(i);
                if (index > -1) {
                    this.condition.splice(index, 1);
                }
            }
        }

        this.activeColumnHeader = !this.activeColumnHeader;
        this.headers.forEach((s: TransactionHeader) => {
            if (this.transactionSelected.includes(s.value)) {
                s.cellClass = 'transactionSelected';
            } else {
                s.cellClass = '';
            }
        });
    }

    itemRowBackground(): string {
        return this.editItem ? 'orange lighten-5' : '';
    }

    changeTransactionState(): void {
        this.editItem = !this.editItem;
        if (this.editItem) {
            this.headers = Object.values(this.headersMap);
        } else {
            this.transactionSelected.forEach((s: string) => {
                this.headers = this.headers.filter(
                    (h: TransactionHeader) => h.value !== s
                );
            });
        }
    }
}
</script>
