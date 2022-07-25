<template>
    <v-container fluid class="background" style="min-height: 100vh">
        <header-component :is-back="false"></header-component>
        <v-row justify="center">
            <v-col cols="12" md="6" class="ma-4">
                <v-card flat class="mx-auto mt-4 mb-0">
                    <v-card-title>
                        <v-row>
                            <v-col cols="12" class="text-caption px-4 py-2">
                                取引番号：000000000000000
                            </v-col>
                            <v-col cols="auto" class="pl-4 pt-0 pr-2 pb-4">
                                <v-icon large color="grey lighten-1">
                                    trending_flat
                                </v-icon>
                            </v-col>
                            <v-col class="pl-2 pt-0 pr-4 pb-4">
                                <div class="text-body-2">カード付替</div>
                                <div class="text-caption">
                                    2021年4月19日 13:00
                                </div>
                            </v-col>
                        </v-row>
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text class="pa-4 text-body-2">
                        <v-row align="center" align-content="center">
                            <v-col cols="5" class="pa-4 pr-3 text-center">
                                <v-img
                                    class="mx-auto"
                                    width="100%"
                                    max-width="80"
                                    src="../assets/kcard.png"
                                ></v-img>
                                <div class="text--primary">ABCカード</div>
                                <div class="text-caption">
                                    カード番号：下4桁6789
                                </div>
                            </v-col>
                            <v-col cols="2" class="px-0 text-center">
                                <v-icon color="grey darken-1">
                                    trending_flat
                                </v-icon>
                            </v-col>
                            <v-col cols="5" class="pa-4 pl-3 text-center">
                                <v-img
                                    class="mx-auto"
                                    width="100%"
                                    max-width="80"
                                    src="../assets/kcard.png"
                                ></v-img>
                                <div class="text--primary">XYZカード</div>
                                <div class="text-caption">
                                    カード番号：下4桁1234
                                </div>
                            </v-col>
                        </v-row>
                    </v-card-text>
                    <v-divider></v-divider>
                    <v-card-text class="px-4 py-2">
                        <div class="text-body-2 text--primary">
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">
                                    付替チャージ残高
                                </v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    1,000,000円
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">
                                    付替ボーナス残高
                                </v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    1,000pt
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">
                                    付替商品交換ボーナス残高
                                </v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    10pt
                                </v-col>
                            </v-row>
                        </div>
                    </v-card-text>
                </v-card>

                <v-divider class="mx-auto my-4"></v-divider>

                <v-card flat class="ma-auto">
                    <v-card-title class="py-2">
                        <v-col cols="auto" class="pa-0">
                            <v-icon large color="grey lighten-1">clear</v-icon>
                        </v-col>
                        <v-col
                            class="text-subtitle-2 font-weight-bold px-2 py-2"
                        >
                            付替不可残高
                        </v-col>
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text class="px-4 py-2">
                        <div class="text-body-2 text--primary">
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">
                                    付替商品交換ボーナス残高
                                </v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    10pt
                                </v-col>
                            </v-row>
                        </div>
                    </v-card-text>
                </v-card>

                <v-card flat class="mx-auto my-4">
                    <v-card-title>
                        <v-row>
                            <v-col cols="12" class="text-caption px-4 py-2">
                                取引番号：000000000000000
                            </v-col>
                            <v-col cols="auto" class="pl-4 pt-0 pr-2 pb-4">
                                <v-icon large color="#FFAC8E">
                                    add_circle_outline
                                </v-icon>
                            </v-col>
                            <v-col cols="auto" class="pl-2 pt-0 pr-4 pb-4">
                                <div class="text-body-2">チャージ</div>
                                <div class="text-caption">
                                    2021年4月19日 13:00
                                </div>
                            </v-col>
                            <v-col class="pl-2 pt-0 pr-4 pb-4 text-right">
                                <span class="text-h6">+1,000</span>
                                <span class="text-body-2 font-weight-bold">
                                    円
                                </span>
                            </v-col>
                        </v-row>
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text class="pa-4 text-body-2">
                        <div class="text-body-2 text--primary">
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">
                                    <div class="text-body-2">
                                        ボーナス付与予定数
                                    </div>
                                    <div class="text-caption">
                                        付与予定日：2021年4月19日 13:00
                                    </div>
                                </v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    +10pt
                                </v-col>
                            </v-row>
                        </div>
                    </v-card-text>
                </v-card>

                <v-card flat class="mx-auto my-4">
                    <v-card-title>
                        <v-row>
                            <v-col cols="12" class="text-caption px-4 py-2">
                                取引番号：000000000000000
                            </v-col>
                            <v-col cols="auto" class="pl-4 pt-0 pr-2 pb-4">
                                <v-icon large color="grey lighten-1">
                                    clear
                                </v-icon>
                            </v-col>
                            <v-col cols="auto" class="pl-2 pt-0 pr-4 pb-4">
                                <div class="text-body-2">チャージ取消</div>
                                <div class="text-caption">
                                    2021年4月19日 13:00
                                </div>
                            </v-col>
                            <v-col class="pl-2 pt-0 pr-4 pb-4 text-right">
                                <span class="text-h6">-1,000</span>
                                <span class="text-body-2 font-weight-bold">
                                    円
                                </span>
                            </v-col>
                        </v-row>
                    </v-card-title>
                </v-card>
                <v-divider class="mx-auto my-4"></v-divider>

                <v-card flat class="ma-auto">
                    <v-card-title class="py-2">
                        <v-col cols="auto" class="pa-0">
                            <v-icon large color="grey lighten-1">clear</v-icon>
                        </v-col>
                        <v-col
                            class="text-subtitle-2 font-weight-bold px-2 py-2"
                        >
                            取消対象取引
                        </v-col>
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text class="px-4 py-2">
                        <div class="text-body-2 text--primary">
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">取引番号</v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    00000000000000
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">取引日時</v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    2021年4月30日 11:00
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">取引種別</v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    チャージ
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">
                                    チャージ残高
                                </v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    +1,000円
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">
                                    <div class="text-body-2">
                                        ボーナス付与予定数
                                    </div>
                                    <div class="text-caption">
                                        付与予定日：2021年4月19日 13:00
                                    </div>
                                </v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    +10pt
                                </v-col>
                            </v-row>
                        </div>
                    </v-card-text>
                </v-card>

                <v-card flat class="mx-auto my-4">
                    <v-card-title>
                        <v-row>
                            <v-col cols="12" class="text-caption px-4 py-2">
                                取引番号：000000000000000
                            </v-col>
                            <v-col cols="auto" class="pl-4 pt-0 pr-2 pb-4">
                                <v-icon large color="#8BCEF6">
                                    check_circle_outline
                                </v-icon>
                            </v-col>
                            <v-col cols="auto" class="pl-2 pt-0 pr-4 pb-4">
                                <div class="text-body-2">支払い</div>
                                <div class="text-caption">
                                    2021年4月19日 13:00
                                </div>
                            </v-col>
                            <v-col class="pl-2 pt-0 pr-4 pb-4 text-right">
                                <span class="text-h6">-1,000</span>
                                <span class="text-body-2 font-weight-bold">
                                    円
                                </span>
                            </v-col>
                        </v-row>
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text class="pa-4 text-body-2">
                        <div class="text-body-2 text--primary">
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">
                                    利用チャージ残高
                                </v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    -200円
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">
                                    利用ボーナス残高
                                </v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    -300pt
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">
                                    <div class="text-body-2">
                                        ボーナス付与予定数
                                    </div>
                                    <div class="text-caption">
                                        付与予定日：2021年4月19日 13:00
                                    </div>
                                </v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    +10pt
                                </v-col>
                            </v-row>
                        </div>
                    </v-card-text>
                </v-card>

                <v-card flat class="mx-auto my-4">
                    <v-card-title>
                        <v-row>
                            <v-col cols="12" class="text-caption px-4 py-2">
                                取引番号：000000000000000
                            </v-col>
                            <v-col cols="auto" class="pl-4 pt-0 pr-2 pb-4">
                                <v-icon large color="grey lighten-1">
                                    clear
                                </v-icon>
                            </v-col>
                            <v-col cols="auto" class="pl-2 pt-0 pr-4 pb-4">
                                <div class="text-body-2">支払い取消</div>
                                <div class="text-caption">
                                    2021年4月19日 13:00
                                </div>
                            </v-col>
                            <v-col class="pl-2 pt-0 pr-4 pb-4 text-right">
                                <span class="text-h6">+1,000</span>
                                <span class="text-body-2 font-weight-bold">
                                    円
                                </span>
                            </v-col>
                        </v-row>
                    </v-card-title>
                </v-card>
                <v-divider class="mx-auto my-4"></v-divider>

                <v-card flat class="ma-auto">
                    <v-card-title class="py-2">
                        <v-col cols="auto" class="pa-0">
                            <v-icon large color="grey lighten-1">clear</v-icon>
                        </v-col>
                        <v-col
                            class="text-subtitle-2 font-weight-bold px-2 py-2"
                        >
                            取消対象取引
                        </v-col>
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text class="px-4 py-2">
                        <div class="text-body-2 text--primary">
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">取引番号</v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    00000000000000
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">取引日時</v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    2021年4月30日 11:00
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">取引種別</v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    支払い
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">
                                    利用チャージ残高
                                </v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    -200円
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">
                                    利用ボーナス残高
                                </v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    -300pt
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">
                                    <div class="text-body-2">
                                        ボーナス付与予定数
                                    </div>
                                    <div class="text-caption">
                                        付与予定日：2021年4月19日 13:00
                                    </div>
                                </v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    +10pt
                                </v-col>
                            </v-row>
                        </div>
                    </v-card-text>
                </v-card>

                <v-card flat class="mx-auto my-4">
                    <v-card-title>
                        <v-row>
                            <v-col cols="12" class="text-caption px-4 py-2">
                                取引番号：000000000000000
                            </v-col>
                            <v-col cols="auto" class="pl-4 pt-0 pr-2 pb-4">
                                <v-icon large color="#8BCEF6">
                                    check_circle_outline
                                </v-icon>
                            </v-col>
                            <v-col cols="auto" class="pl-2 pt-0 pr-4 pb-4">
                                <div class="text-body-2">ボーナス利用</div>
                                <div class="text-caption">
                                    2021年4月19日 13:00
                                </div>
                            </v-col>
                            <v-col class="pl-2 pt-0 pr-4 pb-4 text-right">
                                <span class="text-h6">-200</span>
                                <span class="text-body-2 font-weight-bold">
                                    pt
                                </span>
                            </v-col>
                        </v-row>
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text class="pa-4 text-body-2">
                        <div class="text-body-2 text--primary">
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">
                                    利用ボーナス残高
                                </v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    -200pt
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">
                                    <div class="text-body-2">
                                        ボーナス付与予定数
                                    </div>
                                    <div class="text-caption">
                                        付与予定日：2021年4月19日 13:00
                                    </div>
                                </v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    +10pt
                                </v-col>
                            </v-row>
                        </div>
                    </v-card-text>
                </v-card>

                <v-card flat class="mx-auto my-4">
                    <v-card-title>
                        <v-row>
                            <v-col cols="12" class="text-caption px-4 py-2">
                                取引番号：000000000000000
                            </v-col>
                            <v-col cols="auto" class="pl-4 pt-0 pr-2 pb-4">
                                <v-icon large color="grey lighten-1">
                                    clear
                                </v-icon>
                            </v-col>
                            <v-col cols="auto" class="pl-2 pt-0 pr-4 pb-4">
                                <div class="text-body-2">ボーナス利用取消</div>
                                <div class="text-caption">
                                    2021年4月19日 13:00
                                </div>
                            </v-col>
                            <v-col class="pl-2 pt-0 pr-4 pb-4 text-right">
                                <span class="text-h6">+200</span>
                                <span class="text-body-2 font-weight-bold">
                                    pt
                                </span>
                            </v-col>
                        </v-row>
                    </v-card-title>
                </v-card>
                <v-divider class="mx-auto my-4"></v-divider>

                <v-card flat class="ma-auto">
                    <v-card-title class="py-2">
                        <v-col cols="auto" class="pa-0">
                            <v-icon large color="grey lighten-1">clear</v-icon>
                        </v-col>
                        <v-col
                            class="text-subtitle-2 font-weight-bold px-2 py-2"
                        >
                            取消対象取引
                        </v-col>
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text class="px-4 py-2">
                        <div class="text-body-2 text--primary">
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">取引番号</v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    00000000000000
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">取引日時</v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    2021年4月30日 11:00
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">取引種別</v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    ボーナス利用
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">
                                    利用ボーナス残高
                                </v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    -200pt
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">
                                    <div class="text-body-2">
                                        ボーナス付与予定数
                                    </div>
                                    <div class="text-caption">
                                        付与予定日：2021年4月19日 13:00
                                    </div>
                                </v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    +10pt
                                </v-col>
                            </v-row>
                        </div>
                    </v-card-text>
                </v-card>
                <v-card flat class="mx-auto my-4">
                    <v-card-title>
                        <v-row>
                            <v-col cols="12" class="text-caption px-4 py-2">
                                取引番号：000000000000000
                            </v-col>
                            <v-col cols="auto" class="pl-4 pt-0 pr-2 pb-4">
                                <v-icon large color="#FFAC8E">
                                    add_circle_outline
                                </v-icon>
                            </v-col>
                            <v-col cols="auto" class="pl-2 pt-0 pr-4 pb-4">
                                <div class="text-body-2">ボーナス付与</div>
                                <div class="text-caption">
                                    2021年4月19日 13:00
                                </div>
                            </v-col>
                            <v-col class="pl-2 pt-0 pr-4 pb-4 text-right">
                                <span class="text-h6">+200</span>
                                <span class="text-body-2 font-weight-bold">
                                    pt
                                </span>
                            </v-col>
                        </v-row>
                    </v-card-title>
                </v-card>

                <v-card flat class="mx-auto my-4">
                    <v-card-title>
                        <v-row>
                            <v-col cols="12" class="text-caption px-4 py-2">
                                取引番号：000000000000000
                            </v-col>
                            <v-col cols="auto" class="pl-4 pt-0 pr-2 pb-4">
                                <v-icon large color="grey lighten-1">
                                    clear
                                </v-icon>
                            </v-col>
                            <v-col cols="auto" class="pl-2 pt-0 pr-4 pb-4">
                                <div class="text-body-2">ボーナス付与取消</div>
                                <div class="text-caption">
                                    2021年4月19日 13:00
                                </div>
                            </v-col>
                            <v-col class="pl-2 pt-0 pr-4 pb-4 text-right">
                                <span class="text-h6">-200</span>
                                <span class="text-body-2 font-weight-bold">
                                    円
                                </span>
                            </v-col>
                        </v-row>
                    </v-card-title>
                </v-card>
                <v-divider class="mx-auto my-4"></v-divider>

                <v-card flat class="ma-auto">
                    <v-card-title class="py-2">
                        <v-col cols="auto" class="pa-0">
                            <v-icon large color="grey lighten-1">clear</v-icon>
                        </v-col>
                        <v-col
                            class="text-subtitle-2 font-weight-bold px-2 py-2"
                        >
                            取消対象取引
                        </v-col>
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text class="px-4 py-2">
                        <div class="text-body-2 text--primary">
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">取引番号</v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    00000000000000
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">取引日時</v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    2021年4月30日 11:00
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">取引種別</v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    ボーナス付与
                                </v-col>
                            </v-row>
                            <v-row class="py-2 ma-0" align="center">
                                <v-col cols="auto" class="pa-0">
                                    ボーナス残高
                                </v-col>
                                <v-col class="text-body-1 text-right pa-0">
                                    +200pt
                                </v-col>
                            </v-row>
                        </div>
                    </v-card-text>
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
    name: 'HistoryDetail',
    components: { 'header-component': Header, 'footer-component': Footer },

    data: () => ({
        dialog: false, // ダイアログ表示非表示切り替え
        isCardNumberDisplay: false, // カード番号表示非表示切り替え
        isPINNumberDisplay: false, // PIN番号表示非表示切り替え
    }),
});
</script>
