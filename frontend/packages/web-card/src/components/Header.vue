<template>
    <v-app-bar color="white" height="64" dense elevation="3" app fixed>
        <v-row class="mx-n4" align="center" justify="space-between" no-gutters>
            <v-col v-if="isBack" cols="auto">
                <v-btn icon @click="transitionPreviousPage()">
                    <v-icon class="pa-0 ml-n1" large>chevron_left</v-icon>
                </v-btn>
            </v-col>
            <v-col cols="auto" :offset="isBack ? 0 : 1">
                <v-avatar color="secondary" size="39">
                    <v-img :src="serviceLogoUrl" alt="" />
                </v-avatar>
            </v-col>
            <v-col class="ml-3" cols="auto">
                <div class="text-subtitle-2">
                    {{ providerName }}
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
                            <v-list-item-title
                                class="text-body-2"
                                @click="handleLogout()"
                            >
                                ログアウト
                            </v-list-item-title>
                        </v-list-item>
                    </v-list>
                </v-menu>
            </v-col>
        </v-row>
    </v-app-bar>
</template>
<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { mapGetters } from 'vuex';
import { expireAuthToken } from '../domains/common';

@Component({
    computed: {
        ...mapGetters(['providerName', 'serviceLogoUrl']),
    },
})
export default class Header extends Vue {
    @Prop({ type: Boolean, default: true }) readonly isBack!: boolean;
    protected providerName!: string;
    protected serviceLogoUrl!: string;
    transitionPreviousPage(): void {
        this.$router.go(-1);
    }
    handleLogout(): void {
        expireAuthToken().finally(() => {
            this.$router.push({ name: 'Login' });
        });
    }
}
</script>
