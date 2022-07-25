<template>
    <v-container fluid class="background" style="min-height: 100vh">
        <header-component :is-back="true"></header-component>
        <v-row justify="center">
            <v-col cols="12" md="6" class="ma-4">
                <!-- チャージ残高 -->
                <v-card class="pt-4 mb-4" flat>
                    <v-row
                        class="pb-4"
                        justify="space-between"
                        align="center"
                        no-gutters
                    >
                        <v-col cols="auto">
                            <v-card-text
                                class="font-weight-bold text-subtitle-2 py-0"
                            >
                                チャージ残高
                            </v-card-text>
                        </v-col>
                        <v-col cols="auto">
                            <v-card-text class="font-weight-bold text-h5 py-0">
                                {{ charge.balance.toLocaleString() }}
                                <span class="font-weight-bold text-body-1">
                                    円
                                </span>
                            </v-card-text>
                        </v-col>
                    </v-row>
                    <template v-if="charge.isUseLimit">
                        <v-divider class="mb-4"></v-divider>
                        <v-row justify="end" align="center" no-gutters>
                            <v-col cols="auto">
                                <v-card-text class="text-body-1 py-0">
                                    <span>
                                        {{ chargeBalanceWithoutLimit }}
                                    </span>
                                    <span>円</span>
                                </v-card-text>
                            </v-col>
                        </v-row>
                        <v-row
                            justify="space-between"
                            align="center"
                            no-gutters
                        >
                            <v-col cols="auto">
                                <v-card-text class="text-subtitle-2">
                                    <v-btn class="pa-0 ma-0" href="" text>
                                        うち期間・用途限定
                                        <v-icon color="grey darken-1">
                                            chevron_right
                                        </v-icon>
                                    </v-btn>
                                </v-card-text>
                            </v-col>
                            <v-col cols="auto">
                                <v-card-text class="text-body-1">
                                    <span>
                                        {{ charge.limit.toLocaleString() }}
                                    </span>
                                    <span>円</span>
                                </v-card-text>
                            </v-col>
                        </v-row>
                    </template>
                </v-card>
                <!-- ボーナス残高 -->
                <v-card class="pt-4 mb-4" flat>
                    <v-row
                        class="pb-4"
                        justify="space-between"
                        align="center"
                        no-gutters
                    >
                        <v-col cols="auto">
                            <v-card-text
                                class="font-weight-bold text-subtitle-2 py-0"
                            >
                                ボーナス残高
                            </v-card-text>
                        </v-col>
                        <v-col cols="auto">
                            <v-card-text class="font-weight-bold text-h5 py-0">
                                {{ bonus.balance.toLocaleString() }}
                                <span class="font-weight-bold text-body-1">
                                    pt
                                </span>
                            </v-card-text>
                        </v-col>
                    </v-row>
                    <template v-if="bonus.isUseLimit">
                        <v-divider class="mb-4"></v-divider>
                        <v-row justify="end" align="center" no-gutters>
                            <v-col cols="auto">
                                <v-card-text class="text-body-1 py-0">
                                    <span>
                                        {{ bonusBalanceWithoutLimit }}
                                    </span>
                                    <span>pt</span>
                                </v-card-text>
                            </v-col>
                        </v-row>
                        <v-row
                            justify="space-between"
                            align="center"
                            no-gutters
                        >
                            <v-col cols="auto">
                                <v-card-text class="text-subtitle-2">
                                    <v-btn class="pa-0 ma-0" href="" text>
                                        うち期間・用途限定
                                        <v-icon color="grey darken-1">
                                            chevron_right
                                        </v-icon>
                                    </v-btn>
                                </v-card-text>
                            </v-col>
                            <v-col cols="auto">
                                <v-card-text class="text-body-1">
                                    <span>
                                        {{ bonus.limit.toLocaleString() }}
                                    </span>
                                    <span>pt</span>
                                </v-card-text>
                            </v-col>
                        </v-row>
                    </template>
                </v-card>
                <!-- 商品交換ボーナス -->
                <v-card class="pt-4 mb-4" flat>
                    <v-row
                        class="pb-4"
                        justify="space-between"
                        align="center"
                        no-gutters
                    >
                        <v-col cols="auto">
                            <v-card-text
                                class="font-weight-bold text-subtitle-2 py-0"
                            >
                                決済利用不可ボーナス残高
                            </v-card-text>
                        </v-col>
                        <v-col cols="auto">
                            <v-card-text class="font-weight-bold text-h5 py-0">
                                {{ exchangeProduct.balance.toLocaleString() }}
                                <span class="font-weight-bold text-body-1">
                                    pt
                                </span>
                            </v-card-text>
                        </v-col>
                    </v-row>
                    <template v-if="exchangeProduct.isUseLimit">
                        <v-divider class="mb-4"></v-divider>
                        <v-row justify="end" align="center" no-gutters>
                            <v-col cols="auto">
                                <v-card-text class="text-body-1 py-0">
                                    <span>
                                        {{ exchangeProductBalanceWithoutLimit }}
                                    </span>
                                    <span>pt</span>
                                </v-card-text>
                            </v-col>
                        </v-row>
                        <v-row
                            justify="space-between"
                            align="center"
                            no-gutters
                        >
                            <v-col cols="auto">
                                <v-card-text class="text-subtitle-2">
                                    <v-btn class="pa-0 ma-0" href="" text>
                                        うち期間・用途限定
                                        <v-icon color="grey darken-1">
                                            chevron_right
                                        </v-icon>
                                    </v-btn>
                                </v-card-text>
                            </v-col>
                            <v-col cols="auto">
                                <v-card-text class="text-body-1">
                                    <span>
                                        {{
                                            exchangeProduct.limit.toLocaleString()
                                        }}
                                    </span>
                                    <span>pt</span>
                                </v-card-text>
                            </v-col>
                        </v-row>
                    </template>
                </v-card>
                <!-- ボーナス付与予定 -->
                <template v-if="scheduledBonus.isSetting">
                    <v-divider class="my-4"></v-divider>
                    <v-row justify="center">
                        <v-col cols="12">
                            <v-card flat>
                                <v-card-title>
                                    <v-icon
                                        color="#FFB100"
                                        large
                                        @click="
                                            scheduledBonus.isExist =
                                                !scheduledBonus.isExist
                                        "
                                    >
                                        add_circle_outline
                                    </v-icon>
                                    <div
                                        class="
                                            font-weight-bold
                                            text-subtitle-2
                                            ml-4
                                        "
                                    >
                                        ボーナス付与予定
                                    </div>
                                </v-card-title>
                                <v-divider class="mb-4"></v-divider>
                                <template v-if="scheduledBonus.isExist">
                                    <v-row
                                        v-for="item in scheduledBonus.balance"
                                        :key="item.id"
                                        justify="space-between"
                                        align="center"
                                        class="pl-4 pr-3 pb-4"
                                        no-gutters
                                    >
                                        <v-col cols="auto">
                                            <v-card-text
                                                class="pa-0 text-body-1"
                                            >
                                                {{ item.type }}
                                            </v-card-text>
                                            <v-card-text
                                                class="pa-0 text-caption"
                                                style="opacity: 0.6"
                                            >
                                                付与予定日：{{ item.date }}
                                            </v-card-text>
                                        </v-col>
                                        <v-col
                                            cols="auto"
                                            class="font-weight-bold"
                                        >
                                            <span class="text-h6">
                                                {{ item.point }}
                                            </span>
                                            <span class="text-body-1">pt</span>
                                        </v-col>
                                    </v-row>
                                </template>
                                <template v-else>
                                    <v-row justify="center" no-gutters>
                                        <v-col cols="auto" class="text-center">
                                            <v-icon
                                                color="#000000"
                                                style="
                                                    opacity: 0.12;
                                                    font-size: 60px;
                                                "
                                            >
                                                history
                                            </v-icon>
                                        </v-col>
                                    </v-row>
                                    <v-row justify="center" no-gutters>
                                        <v-col
                                            cols="auto"
                                            class="text-center pb-4"
                                        >
                                            <v-card-text
                                                class="text-body-1"
                                                style="opacity: 0.6"
                                            >
                                                ボーナス付与予定がありません
                                            </v-card-text>
                                        </v-col>
                                    </v-row>
                                </template>
                            </v-card>
                        </v-col>
                    </v-row>
                </template>
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
    name: 'BalanceList',
    components: { 'header-component': Header, 'footer-component': Footer },
    data: () => ({
        charge: {
            balance: 770,
            isUseLimit: true,
            limit: 270,
        },
        bonus: {
            balance: 5500,
            isUseLimit: true,
            limit: 270,
        },
        exchangeProduct: {
            balance: 200,
            isUseLimit: false,
            limit: 0,
        },
        scheduledBonus: {
            isSetting: true,
            isExist: true,
            balance: [
                {
                    id: 1,
                    type: '決済利用不可ボーナス',
                    date: '2021年4月19日 13:00',
                    point: 20,
                },
                {
                    id: 2,
                    type: 'ボーナス',
                    date: '2021年4月19日 13:00',
                    point: 30,
                },
                {
                    id: 3,
                    type: '決済利用不可ボーナス',
                    date: '2021年4月19日 13:00',
                    point: 20,
                },
            ],
        },
    }),
    computed: {
        chargeBalanceWithoutLimit() {
            return (this.charge.balance - this.charge.limit).toLocaleString();
        },
        bonusBalanceWithoutLimit() {
            return (this.bonus.balance - this.bonus.limit).toLocaleString();
        },
        exchangeProductBalanceWithoutLimit() {
            return (
                this.exchangeProduct.balance - this.exchangeProduct.limit
            ).toLocaleString();
        },
    },
});
</script>
