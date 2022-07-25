import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import Top from '../views/Top.vue';
import History from '../views/History.vue';
import CardList from '../views/CardList.vue';
import HistoryApprovalDecision from '../views/HistoryApprovalDecision.vue';
import CardDetail from '../views/CardDetail.vue';
import CsvDownload from '../views/CsvDownload.vue';
import TransactionStatistic from '../views/TransactionStatistic.vue';
import Error403 from '../views/Error403.vue';
import Error404 from '../views/Error404.vue';
import Error500 from '../views/Error500.vue';
import Error503 from '../views/Error503.vue';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
    {
        path: '/',
        name: 'Top',
        component: Top,
        meta: { requiresAuth: true },
        children: [
            {
                path: '/history',
                name: 'History',
                component: History,
                meta: { requiresAuth: true },
            },
            {
                path: '/cardList',
                name: 'CardList',
                component: CardList,
                meta: { requiresAuth: true },
            },
            {
                path: '/historyApprovalDecision',
                name: 'HistoryApprovalDecision',
                component: HistoryApprovalDecision,
                meta: { requiresAuth: true },
            },
            {
                path: 'transactionStatistic',
                name: 'TransactionStatistic',
                component: TransactionStatistic,
                meta: { requiresAuth: true },
            },
            {
                path: '/cardDetail',
                name: 'CardDetail',
                component: CardDetail,
                meta: { requiresAuth: true },
            },
            {
                path: '/csvDownload',
                name: 'CsvDownload',
                component: CsvDownload,
            },
        ],
    },
    {
        path: '/login',
        name: 'Login',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () =>
            import(/* webpackChunkName: "login" */ '../views/Login.vue'),
    },
    // TODO:初期パスワード変更 箇所
    {
        path: '/initialPasswordChange',
        name: 'InitialPasswordChange',
        component: () =>
            import(
                /* webpackChunkName: "passwordChange" */ '../views/InitialPasswordChange.vue'
            ),
    },
    {
        path: '/403',
        name: 'Error403',
        component: Error403,
    },
    {
        path: '*',
        name: 'Error404',
        component: Error404,
    },
    {
        path: '/500',
        name: 'Error500',
        component: Error500,
    },
    {
        path: '/503',
        name: 'Error503',
        component: Error503,
    },
];

const router = new VueRouter({
    routes,
});

router.beforeEach((to, from, next) => {
    const loggedIn = localStorage.getItem('auth');
    if (to.matched.some((record) => record.meta.requiresAuth)) {
        if (!loggedIn) {
            next({
                path: '/Login',
                query: { redirect: to.fullPath },
            });
        } else {
            next();
        }
    } else {
        next();
    }
});

export default router;
