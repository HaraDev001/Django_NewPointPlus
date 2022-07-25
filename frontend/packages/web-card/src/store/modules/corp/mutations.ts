import { Mutations } from 'vuex';
import { MutationsInterface, StateInterface } from './type';

const mutations: Mutations<StateInterface, MutationsInterface> = {
    setCorpInfo(state, payload) {
        state.providerName = payload.providerName;
        state.serviceLogoUrl = payload.serviceLogoUrl;
        state.serviceName = payload.serviceName;
    },
};

export { mutations };
