import { Getters } from 'vuex';
import { GettersInterface, StateInterface } from './type';

const getters: Getters<StateInterface, GettersInterface> = {
    providerName(state) {
        return state.providerName;
    },
    serviceLogoUrl(state) {
        return state.serviceLogoUrl;
    },
    serviceName(state) {
        return state.serviceName;
    },
};

export { getters };
