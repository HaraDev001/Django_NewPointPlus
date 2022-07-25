<template>
    <v-container fluid class="background" style="min-height: 100vh">
        <header-component :is-back="false"></header-component>
        <v-row justify="center">
            <v-col cols="12" md="6" class="ma-4">
                <v-card
                    v-for="list in limitList"
                    :key="list.id"
                    class="py-4 mb-4"
                    elevation="0"
                    flat
                >
                    <v-row justify="space-between" align="center" no-gutters>
                        <v-col cols="auto">
                            <v-card-text class="text-body-1 py-0 pr-0">
                                <span>{{ list.restriction }}</span>
                                <v-dialog
                                    v-model="list.dialog"
                                    width="358"
                                    min-width="358"
                                >
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn
                                            v-if="list.link"
                                            class="pa-0"
                                            icon
                                            v-bind="attrs"
                                            v-on="on"
                                        >
                                            <v-icon style="opacity: 0.6">
                                                error
                                            </v-icon>
                                        </v-btn>
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
                                                    利用可能店舗
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
                                                            @click="
                                                                list.dialog = false
                                                            "
                                                        >
                                                            <v-icon>
                                                                clear
                                                            </v-icon>
                                                        </v-btn>
                                                    </v-card-actions>
                                                </v-col>
                                            </v-row>
                                        </v-card-title>
                                        <v-divider></v-divider>
                                        <v-card-text
                                            v-for="dialogAreaContent in list.dialogAreaContents"
                                            :key="dialogAreaContent.id"
                                            class="pa-2 pr-1"
                                        >
                                            <div
                                                class="
                                                    text-body-2
                                                    font-weight-bold
                                                    pa-2
                                                "
                                            >
                                                {{
                                                    dialogAreaContent.areaTitle
                                                }}
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
                                                {{
                                                    dialogAreaContent.areaContent
                                                }}
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
                                            利用可能期限
                                        </v-card-title>
                                        <v-divider></v-divider>
                                        <v-card-text class="pa-2">
                                            <div
                                                class="
                                                    text-body-1 text--primary
                                                "
                                            >
                                                <v-row
                                                    v-for="dialogPeriodContent in list.dialogPeriodContents"
                                                    :key="
                                                        dialogPeriodContent.id
                                                    "
                                                    class="pl-4 ma-0"
                                                    align="center"
                                                >
                                                    <v-col
                                                        class="text-body-2 pa-2"
                                                    >
                                                        {{
                                                            dialogPeriodContent.period
                                                        }}
                                                    </v-col>
                                                    <v-col
                                                        class="
                                                            font-weight-bold
                                                            py-0
                                                            text-right
                                                        "
                                                    >
                                                        <span class="text-h6">
                                                            {{
                                                                dialogPeriodContent.amount
                                                            }}
                                                        </span>
                                                        円
                                                    </v-col>
                                                </v-row>
                                            </div>
                                        </v-card-text>
                                    </v-card>
                                </v-dialog>
                            </v-card-text>
                        </v-col>
                        <v-col cols="auto">
                            <v-card-text class="font-weight-bold text-h5 py-0">
                                {{ list.balance }}
                                <span class="font-weight-bold text-body-1">
                                    円
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
    name: 'BalanceDetail',
    components: { 'header-component': Header, 'footer-component': Footer },
    data: () => ({
        limitList: [
            {
                id: 1,
                restriction: '武蔵野店、その他20店',
                link: true,
                balance: 270,
                dialog: false,
                dialogAreaContents: [
                    {
                        id: 1,
                        areaTitle: '関東',
                        areaContent:
                            '武蔵野店 / 新宿店 / 渋谷店 / 池袋店 / 東京店 / 丸の内店 / 秋葉原店 / 中野店 / 北千住店 / 豊洲店 / 自由が丘店 / 立川店 / 町田店 / 調布店',
                    },
                    {
                        id: 2,
                        areaTitle: '中部',
                        areaContent:
                            '長野店 / 静岡店 / 浜松店 / 名古屋店 / 桑名店 / 金沢店',
                    },
                ],
                dialogPeriodContents: [
                    {
                        id: 1,
                        period: '2021年4月28日まで',
                        amount: '150',
                    },
                    {
                        id: 2,
                        period: '2021年4月30日まで',
                        amount: '100',
                    },
                    {
                        id: 3,
                        period: '2021年5月10日まで',
                        amount: '20',
                    },
                ],
            },
            {
                id: 2,
                restriction: 'ムサシドラッグ店',
                link: false,
                balance: 100,
                dialog: false,
                dialogAreaContents: [
                    {
                        id: 0,
                        areaTitle: '',
                        areaContent: '',
                    },
                ],
                dialogPeriodContents: [
                    {
                        id: 0,
                        period: '',
                        amount: '',
                    },
                ],
            },
            {
                id: 3,
                restriction: '2021年9月1日まで',
                link: false,
                balance: 400,
                dialog: false,
                dialogAreaContents: [
                    {
                        id: 0,
                        areaTitle: '',
                        areaContent: '',
                    },
                ],
                dialogPeriodContents: [
                    {
                        id: 0,
                        period: '',
                        amount: '',
                    },
                ],
            },
            {
                id: 4,
                restriction: '綾瀬店',
                link: true,
                balance: 270,
                dialog: false,
                dialogAreaContents: [
                    {
                        id: 1,
                        areaTitle: '関東',
                        areaContent: '関東 / 関東 / 関東 / 関東 / 関東',
                    },
                    {
                        id: 2,
                        areaTitle: '中部',
                        areaContent: '中部 / 中部 / 中部 / 中部 / 中部',
                    },
                ],
                dialogPeriodContents: [
                    {
                        id: 1,
                        period: '2021年4月28日まで',
                        amount: '100',
                    },
                    {
                        id: 2,
                        period: '2021年4月10日まで',
                        amount: '170',
                    },
                ],
            },
            {
                id: 5,
                restriction: '銀座マルイ店',
                link: true,
                balance: 270,
                dialog: false,
                dialogAreaContents: [
                    {
                        id: 1,
                        areaTitle: '関東',
                        areaContent: '関東 / 関東 / 関東 / 関東 / 関東',
                    },
                    {
                        id: 2,
                        areaTitle: '中部',
                        areaContent: '中部 / 中部 / 中部 / 中部 / 中部',
                    },
                ],
                dialogPeriodContents: [
                    {
                        id: 1,
                        period: '2021年4月28日まで',
                        amount: '50',
                    },
                    {
                        id: 2,
                        period: '2021年4月30日まで',
                        amount: '50',
                    },
                    {
                        id: 3,
                        period: '2021年5月10日まで',
                        amount: '170',
                    },
                ],
            },
        ],
    }),
});
</script>
