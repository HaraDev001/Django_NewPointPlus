import { Getters } from 'vuex';
import { GettersInterface, StateInterface } from './type';

const getters: Getters<StateInterface, GettersInterface> = {
    authToken(state) {
        return state.authToken;
    },
    tokenExpirationDate(state) {
        return state.tokenExpirationDate;
    },
    refreshToken(state) {
        return state.refreshToken;
    },
    tokenExpirationDateConvertDate(state) {
        return new Date(state.tokenExpirationDate);
    },
};

export { getters };
