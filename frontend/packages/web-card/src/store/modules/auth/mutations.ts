import { Mutations } from 'vuex';
import { MutationsInterface, StateInterface } from './type';

const mutations: Mutations<StateInterface, MutationsInterface> = {
    setAuth(state, payload) {
        state.authToken = payload.authToken;
        state.tokenExpirationDate = payload.tokenExpirationDate;
        state.refreshToken = payload.refreshToken;
    },
    clearAuth(state) {
        state.authToken = '';
        state.tokenExpirationDate = '';
        state.refreshToken = '';
    },
};

export { mutations };
