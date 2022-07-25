import { Mutations } from 'vuex';
import { MutationsInterface, StateInterface } from './type';

const mutations: Mutations<StateInterface, MutationsInterface> = {
    setAuth(state, payload) {
        localStorage.setItem('auth', JSON.stringify(payload));
    },
    clearAuth() {
        localStorage.removeItem('auth');
    },
};

export { mutations };
