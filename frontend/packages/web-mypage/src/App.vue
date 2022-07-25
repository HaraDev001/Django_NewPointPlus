<template>
    <v-app>
        <v-app-bar
            app
            min-width="960"
            color="grey darken-3"
            height="56"
            dense
            elevation="1"
            dark
            clipped-left
            flat
        >
            <v-row no-gutters align="center">
                <v-col cols="auto">
                    <v-sheet
                        class="d-flex flex-row align-center ml-n4"
                        height="56"
                        width="255"
                        color="white"
                    >
                        <v-sheet class="mx-4" width="24" color="white">
                            <v-icon color="primary" @click="toggleSidebar">
                                menu
                            </v-icon>
                        </v-sheet>
                        <v-sheet width="132" color="white">
                            <v-img
                                src="./assets/cmn/logo.svg"
                                width="132"
                            ></v-img>
                        </v-sheet>
                    </v-sheet>
                </v-col>
                <v-col cols="auto" class="pl-4 d-flex flex-row align-center">
                    <v-avatar size="40">
                        <img src="./assets/cmn/company_icn.png" />
                    </v-avatar>
                    <div class="text-body-1 pl-2">ムサシノスーパー</div>
                </v-col>
                <v-spacer></v-spacer>
                <v-col cols="auto">
                    <v-menu offset-y>
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                color="white"
                                depressed
                                light
                                large
                                v-bind="attrs"
                                v-on="on"
                            >
                                <v-icon light medium left>
                                    account_circle
                                </v-icon>
                                <v-sheet
                                    width="65"
                                    color="transparent"
                                    class="text-left text-body-2"
                                >
                                    山田太郎
                                </v-sheet>
                                <v-icon light medium right>
                                    arrow_drop_down
                                </v-icon>
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
        <v-navigation-drawer
            v-model="drawer"
            color="grey lighten-5"
            app
            clipped
        >
            <v-list nav dense>
                <v-list-group
                    v-for="menu in sidebar"
                    :key="menu.title"
                    v-model="menu.active"
                    :prepend-icon="menu.action"
                    no-action
                    :append-icon="menu.arrow"
                >
                    <template v-slot:activator>
                        <v-list-item-content>
                            <v-list-item-title
                                v-text="menu.title"
                            ></v-list-item-title>
                        </v-list-item-content>
                    </template>
                    <v-list-item
                        v-for="submenu in menu.items"
                        :key="submenu.title"
                        link
                        :to="submenu.link"
                    >
                        <v-list-item-content>
                            <v-list-item-title
                                v-text="submenu.title"
                            ></v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list-group>
            </v-list>
        </v-navigation-drawer>

        <v-main>
            <router-view />
            <v-footer min-width="960" padless color="transparent">
                <div
                    class="text-center text-body-2 text--secondary mx-auto py-4"
                >
                    &copy; arara inc.
                </div>
            </v-footer>
        </v-main>
    </v-app>
</template>

<script lang="ts">
import Vue from 'vue';
export default Vue.extend({
    data: () => ({
        drawer: false,
        group: null,
        sidebar: [
            {
                action: 'point_of_sale',
                arrow: 'arrow_drop_down',
                active: false,
                items: [
                    {
                        title: '取引履歴',
                        link: '',
                    },
                    {
                        title: '取引集計',
                        link: '',
                    },
                ],
                title: '取引',
            },
            {
                action: 'payment',
                arrow: 'arrow_drop_down',
                active: false,
                items: [
                    {
                        title: 'カード管理',
                        link: '#',
                    },
                ],
                title: 'カード',
            },
        ],
    }),
    methods: {
        toggleSidebar: function () {
            this.drawer = !this.drawer;
        },
    },
});
</script>
