<template>
    <v-app class="grey lighten-5">
        <v-app-bar color="white" height="64" dense elevation="3" app fixed>
            <v-row
                class="mx-n4"
                align="center"
                justify="space-between"
                no-gutters
            >
                <v-col cols="auto" class="pl-3">
                    <v-avatar color="secondary" size="39">
                        <v-img :src="company.image" alt="" />
                    </v-avatar>
                </v-col>
                <v-col class="ml-3" cols="auto">
                    <div class="text-subtitle-2">
                        {{ company.name }}
                    </div>
                </v-col>
                <v-spacer></v-spacer>
                <v-col cols="auto">
                    <v-menu offset-y>
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn icon v-bind="attrs" v-on="on">
                                <v-icon>account_circle</v-icon>
                            </v-btn>
                        </template>
                        <v-list dense>
                            <v-list-item link>
                                <v-list-item-title class="text-body-2">
                                    ログアウト
                                </v-list-item-title>
                            </v-list-item>
                        </v-list>
                    </v-menu>
                </v-col>
            </v-row>
        </v-app-bar>
        <v-container fill-height>
            <v-sheet
                max-width="500"
                color="transparent"
                class="ma-auto text-center"
            >
                <div>
                    <div class="text-h5 font-weight-bold">
                        お探しのページが見つかりません
                    </div>
                    <div
                        class="
                            text--secondary
                            font-weight-bold
                            text-body-1
                            pt-1
                        "
                    >
                        エラーコード：404
                    </div>
                </div>
                <div class="text--secondary text-left pt-6">
                    大変申し訳ございませんが、お探しのページは、削除されたか、ファイル名が間違っている可能性があります。
                    <br />
                    アドレスを確認してください。
                </div>
                <div class="pt-8">
                    <v-btn color="grey lighten-2" block elevation="0">
                        前のページに戻る
                    </v-btn>
                </div>
            </v-sheet>
        </v-container>
        <layout-footer></layout-footer>
    </v-app>
</template>
<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import LayoutFooter from '../../components/Footer.vue';

@Component({
    components: { LayoutFooter },
})
export default class ClientErrorPage extends Vue {
    company = {
        image: 'https://placehold.jp/3d4070/ffffff/40x40.png',
        name: 'samplesample',
    };
}
</script>
