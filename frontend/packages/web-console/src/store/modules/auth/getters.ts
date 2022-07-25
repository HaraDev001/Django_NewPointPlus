import { Getters } from 'vuex';
import { GettersInterface, StateInterface } from './type';

const getters: Getters<StateInterface, GettersInterface> = {
    authToken() {
        const auth = JSON.parse(<string>localStorage.getItem('auth'));
        return auth?.authToken;
    },
    tokenExpirationDate() {
        const auth = JSON.parse(<string>localStorage.getItem('auth'));
        return auth?.tokenExpirationDate;
    },
    refreshToken() {
        const auth = JSON.parse(<string>localStorage.getItem('auth'));
        return auth?.refreshToken;
    },
    tokenExpirationDateConvertDate() {
        const auth = JSON.parse(<string>localStorage.getItem('auth'));
        return new Date(auth?.token_expiration_date);
    },
};

export { getters };
