<template>
    <v-app>
        <v-main>
            <router-view />
        </v-main>
    </v-app>
</template>

<script lang="ts">
import * as Vuex from 'vuex';
import { Component, Vue, Watch } from 'vue-property-decorator';
import { Route } from 'vue-router';
import { expireAuthToken, updateAuthToken } from './domains/common';

@Component({ name: 'App' })
export default class App extends Vue {
    $store!: Vuex.ExStore;
    timeoutId = 0;
    @Watch('$route')
    handleNoOperationTimeout(to: Route, from: Route): void {
        if (to.name !== 'Login') {
            if (to.name !== from.name) {
                if (this.timeoutId !== 0) {
                    clearTimeout(this.timeoutId);
                }
                this.timeoutId = setTimeout(
                    () =>
                        // 無操作=画面遷移が6時間ない場合、トークン失効APIを実行する
                        expireAuthToken().finally(() =>
                            // API実行結果に関係なく、ログイン画面に遷移する
                            this.$router.push({ name: 'Login' })
                        ),
                    21600000
                );
            }
        }
    }
    @Watch('$route')
    updateTokenIfExpired(to: Route, from: Route): void {
        if (to.name !== from.name) {
            // 日時比較のため、getTime()で時間数に変換する
            const tokenDeadline =
                this.$store.getters.tokenExpirationDateConvertDate.getTime();
            const now = new Date().getTime();
            // トークン有効期限が切れている = 時間数が少ない場合、トークン更新を行う
            if (tokenDeadline < now) {
                updateAuthToken().catch(() => {
                    this.$router.push({ name: 'Login' });
                });
            }
        }
    }
}
</script>
