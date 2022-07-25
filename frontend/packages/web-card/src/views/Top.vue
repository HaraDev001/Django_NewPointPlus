<template>
    <v-container fluid class="background" style="min-height: 100vh">
        <header-component :is-back="false"></header-component>
        <v-row justify="center">
            <v-col cols="12" md="6" class="ma-4 py-0">
                <v-card class="mb-4 pt-4" flat>
                    <v-card class="mx-12" elevation="3">
                        <v-dialog v-model="dialog" width="358" min-width="358">
                            <template v-slot:activator="{ on, attrs }">
                                <v-img
                                    aspect-ratio="1.586"
                                    contain
                                    src="https://user-images.githubusercontent.com/60082998/125714564-23c2bac2-661c-461b-9455-c9419c51ef68.png"
                                    v-bind="attrs"
                                    v-on="on"
                                ></v-img>
                            </template>
                            <v-card>
                                <v-card-title
                                    class="
                                        text-subtitle-1
                                        font-weight-bold
                                        pa-4
                                        pr-2
                                    "
                                >
                                    <v-row no-gutters>
                                        <v-col
                                            class="pa-0"
                                            style="height: 24px"
                                        >
                                            カード情報
                                        </v-col>
                                        <v-col
                                            class="pa-0"
                                            style="height: 24px"
                                        >
                                            <v-card-actions
                                                class="pa-0 pt-1"
                                                style="height: 24px"
                                            >
                                                <v-spacer></v-spacer>
                                                <v-btn
                                                    icon
                                                    class="pa-0"
                                                    @click="dialog = false"
                                                >
                                                    <v-icon>clear</v-icon>
                                                </v-btn>
                                            </v-card-actions>
                                        </v-col>
                                    </v-row>
                                </v-card-title>
                                <v-divider></v-divider>
                                <v-card-text class="pa-2 pr-1">
                                    <div
                                        class="
                                            text-body-2
                                            font-weight-bold
                                            pa-2
                                        "
                                    >
                                        カード名
                                    </div>
                                    <div
                                        class="
                                            text-body-1
                                            font-weight-bold
                                            text--primary
                                            pa-2
                                            pl-6
                                        "
                                    >
                                        ABCカード
                                    </div>
                                    <div
                                        class="
                                            text-body-2
                                            font-weight-bold
                                            pa-2
                                        "
                                    >
                                        カード番号
                                    </div>
                                    <div
                                        class="
                                            text-body-1
                                            font-weight-bold
                                            text--primary
                                            pa-0
                                            pl-3
                                        "
                                    >
                                        <v-text-field
                                            value="1234123412341234"
                                            dense
                                            readonly
                                            solo
                                            flat
                                            hide-details
                                            :type="
                                                isCardNumberDisplay
                                                    ? 'text'
                                                    : 'password'
                                            "
                                            :append-icon="
                                                isCardNumberDisplay
                                                    ? 'visibility_off'
                                                    : 'remove_red_eye'
                                            "
                                            @click:append="
                                                isCardNumberDisplay =
                                                    !isCardNumberDisplay
                                            "
                                        ></v-text-field>
                                    </div>
                                    <div
                                        class="
                                            text-body-2
                                            font-weight-bold
                                            pa-2
                                        "
                                    >
                                        PIN番号
                                    </div>
                                    <div
                                        class="
                                            text-body-1
                                            font-weight-bold
                                            text--primary
                                            pa-0
                                            pl-3
                                        "
                                    >
                                        <v-text-field
                                            value="1234"
                                            dense
                                            readonly
                                            solo
                                            flat
                                            hide-details
                                            :type="
                                                isPINNumberDisplay
                                                    ? 'text'
                                                    : 'password'
                                            "
                                            :append-icon="
                                                isPINNumberDisplay
                                                    ? 'visibility_off'
                                                    : 'remove_red_eye'
                                            "
                                            @click:append="
                                                isPINNumberDisplay =
                                                    !isPINNumberDisplay
                                            "
                                        ></v-text-field>
                                    </div>
                                </v-card-text>
                                <v-divider></v-divider>
                                <v-card-title
                                    class="
                                        text-subtitle-1
                                        font-weight-bold
                                        px-4
                                        pb-4
                                    "
                                >
                                    取引設定
                                </v-card-title>
                                <v-divider></v-divider>
                                <v-card-text class="pa-2">
                                    <div
                                        class="
                                            text-body-2
                                            font-weight-bold
                                            pa-2
                                        "
                                    >
                                        チャージ上限額
                                    </div>
                                    <div class="text-body-1 text--primary">
                                        <v-row class="pl-4 ma-0" align="center">
                                            <v-col class="text-body-2 pa-2">
                                                1日あたり
                                            </v-col>
                                            <v-col
                                                class="
                                                    font-weight-bold
                                                    py-2
                                                    text-right
                                                "
                                            >
                                                <span class="text-h6">
                                                    20,000
                                                </span>
                                                円
                                            </v-col>
                                        </v-row>
                                        <v-row class="pl-4 ma-0" align="center">
                                            <v-col class="text-body-2 pa-2">
                                                1月あたり
                                            </v-col>
                                            <v-col
                                                class="
                                                    font-weight-bold
                                                    py-2
                                                    text-right
                                                "
                                            >
                                                <span class="text-h6">
                                                    100,000
                                                </span>
                                                円
                                            </v-col>
                                        </v-row>
                                    </div>
                                    <div
                                        class="
                                            text-body-2
                                            font-weight-bold
                                            pa-2
                                        "
                                    >
                                        決済上限額
                                    </div>
                                    <div class="text-body-1 text--primary">
                                        <v-row class="pl-4 ma-0" align="center">
                                            <v-col class="text-body-2 pa-2">
                                                1日あたり
                                            </v-col>
                                            <v-col
                                                class="
                                                    font-weight-bold
                                                    py-2
                                                    text-right
                                                "
                                            >
                                                <span class="text-h6">
                                                    20,000
                                                </span>
                                                円
                                            </v-col>
                                        </v-row>
                                        <v-row class="pl-4 ma-0" align="center">
                                            <v-col class="text-body-2 pa-2">
                                                1月あたり
                                            </v-col>
                                            <v-col
                                                class="
                                                    font-weight-bold
                                                    py-2
                                                    text-right
                                                "
                                            >
                                                <span class="text-h6">
                                                    100,000
                                                </span>
                                                円
                                            </v-col>
                                        </v-row>
                                    </div>
                                </v-card-text>
                            </v-card>
                        </v-dialog>
                    </v-card>
                    <v-layout>
                        <v-card-text>
                            <v-row no-gutters>
                                <v-col cols="6" class="pr-4">
                                    <div class="text-caption text--secondary">
                                        チャージ残高
                                    </div>
                                    <div
                                        class="
                                            font-weight-bold
                                            text-h5 text-right
                                            mt-2
                                        "
                                    >
                                        {{ charge_balance }}
                                        <span
                                            class="
                                                font-weight-bold
                                                text-subtitle-1
                                            "
                                        >
                                            円
                                        </span>
                                    </div>
                                </v-col>
                                <v-divider vertical></v-divider>
                                <v-col cols="6" class="pl-4">
                                    <div class="text-caption text--secondary">
                                        ボーナス残高
                                    </div>
                                    <div
                                        class="
                                            font-weight-bold
                                            text-h5 text-right
                                            mt-2
                                        "
                                    >
                                        {{ bonus_balance }}
                                        <span
                                            class="
                                                font-weight-bold
                                                text-subtitle-1
                                            "
                                        >
                                            pt
                                        </span>
                                    </div>
                                </v-col>
                            </v-row>
                        </v-card-text>
                    </v-layout>
                    <v-btn
                        block
                        light
                        class="text-subtitle-2 rounded-t-0"
                        color="grey lighten-2"
                        height="56"
                        elevation="0"
                        @click="transitionNextPage('BalanceList')"
                    >
                        残高の内訳を確認する
                        <v-icon color="grey darken-1">chevron_right</v-icon>
                    </v-btn>
                </v-card>

                <div class="font-weight-bold text-subtitle-1">取引履歴</div>

                <v-card
                    v-for="(trading_history, index) in trading_histories"
                    :key="index"
                    class="my-4 pa-4"
                    flat
                    href="/historyDetail"
                >
                    <v-row align="center" no-gutters>
                        <v-col cols="2">
                            <v-icon :color="trading_history.color" large>
                                {{ trading_history.icon }}
                            </v-icon>
                        </v-col>
                        <v-col cols="6">
                            <v-card-text class="pa-0">
                                <div class="text-subtitle-1">
                                    {{ trading_history.trading }}
                                </div>
                                <div class="text-caption text--secondary">
                                    {{ trading_history.date }}
                                </div>
                            </v-card-text>
                        </v-col>
                        <v-col cols="4">
                            <v-card-text
                                class="font-weight-bold text-h6 text-right pa-0"
                            >
                                {{ trading_history.price }}
                                <span v-if="trading_history.id == 6"></span>
                                <span
                                    v-else-if="
                                        trading_history.id == 1 ||
                                        trading_history.id == 2 ||
                                        trading_history.id == 3 ||
                                        trading_history.id == 4
                                    "
                                    class="font-weight-bold text-subtitle-1"
                                >
                                    円
                                </span>
                                <span
                                    v-else
                                    class="font-weight-bold text-subtitle-1"
                                >
                                    pt
                                </span>
                            </v-card-text>
                        </v-col>
                    </v-row>
                </v-card>
            </v-col>
        </v-row>
        <footer-component></footer-component>
    </v-container>
</template>

<script lang="ts">
import Vue from 'vue';
import Header from '../components/Header.vue';
import Footer from '../components/Footer.vue';

export default Vue.extend({
    components: { 'header-component': Header, 'footer-component': Footer },
    data() {
        return {
            dialog: false, // ダイアログ表示非表示切り替え
            isCardNumberDisplay: false, // カード番号表示非表示切り替え
            isPINNumberDisplay: false, // PIN番号表示非表示切り替え

            charge_balance: '770',
            bonus_balance: '5,500',
            trading_histories: [
                {
                    id: 1,
                    icon: 'clear',
                    color: 'grey lighten-1',
                    trading: '支払い取消',
                    date: '2021年4月30日 11:01',
                    price: '+1,000',
                },
                {
                    id: 2,
                    icon: 'add_circle_outline',
                    color: '#FFAC8E',
                    trading: 'チャージ',
                    date: '2021年4月28日 11:01',
                    price: '+1,000',
                },
                {
                    id: 3,
                    icon: 'check_circle_outline',
                    color: '#8BCEF6',
                    trading: '支払い',
                    date: '2021年4月30日 11:01',
                    price: '-500',
                },
                {
                    id: 4,
                    icon: 'clear',
                    color: 'grey lighten-1',
                    trading: 'チャージ取消',
                    date: '2021年4月28日 11:01',
                    price: '+1,000',
                },
                {
                    id: 5,
                    icon: 'check_circle_outline',
                    color: '#8BCEF6',
                    trading: 'ボーナス利用',
                    date: '2021年4月20日 11:01',
                    price: '-100',
                },
                {
                    id: 6,
                    icon: 'trending_flat',
                    color: 'grey lighten-1',
                    trading: 'カード付替',
                    date: '2021年4月20日 11:01',
                },
                {
                    id: 7,
                    icon: 'clear',
                    color: 'grey lighten-1',
                    trading: 'ボーナス付与取消',
                    date: '2021年4月20日 11:01',
                    price: '-200',
                },
                {
                    id: 8,
                    icon: 'add_circle_outline',
                    color: '#FFAC8E',
                    trading: 'ボーナス付与',
                    date: '2021年4月28日 11:01',
                    price: '+200',
                },
                {
                    id: 9,
                    icon: 'clear',
                    color: 'grey lighten-1',
                    trading: 'ボーナス利用取消',
                    date: '2021年4月30日 11:01',
                    price: '+200',
                },
            ],
        };
    },
    methods: {
        transitionNextPage(pathName: string) {
            this.$router.push({ name: pathName });
        },
    },
});
</script>
