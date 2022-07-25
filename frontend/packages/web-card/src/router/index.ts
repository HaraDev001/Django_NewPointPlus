import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import Top from '../views/Top.vue';
import Login from '../views/Login.vue';
import BalanceList from '../views/BalanceList.vue';
import BalanceDetail from '../views/BalanceDetail.vue';
import HistoryDetail from '../views/HistoryDetail.vue';
import ClientError404Page from '../views/error/ClientError404Page.vue';
import ServerError500Page from '../views/error/ServerError500Page.vue';
import ServerError503Page from '../views/error/ServerError503Page.vue';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
    {
        path: '/',
        name: 'Top',
        component: Top,
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
    },
    {
        path: '/balance-list',
        name: 'BalanceList',
        component: BalanceList,
    },
    {
        path: '/balance-detail',
        name: 'BalanceDetail',
        component: BalanceDetail,
    },
    {
        path: '/historyDetail',
        name: 'HistoryDetail',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: HistoryDetail,
    },
    {
        path: '/client-error-404',
        name: 'ClientError404Page',
        component: ClientError404Page,
    },
    {
        path: '/server-error-500',
        name: 'ServerError500Page',
        component: ServerError500Page,
    },
    {
        path: '/server-error-503',
        name: 'ServerError503Page',
        component: ServerError503Page,
    },
];

const router = new VueRouter({
    mode: 'history',
    routes,
});

export default router;
