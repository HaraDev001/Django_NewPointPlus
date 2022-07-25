import Vue from 'vue';
import Vuex from 'vuex';
import user from './modules/user';
import auth from './modules/auth';
import corp from './modules/corp';

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        user,
        auth,
        corp,
    },
});
