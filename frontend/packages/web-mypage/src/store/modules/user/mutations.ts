import { Mutations } from 'vuex';
import { MutationsInterface, StateInterface } from './type';

const mutations: Mutations<StateInterface, MutationsInterface> = {
    setId(state, payload) {
        state = { ...state, id: payload };
    },
    setName(state, payload) {
        state = { ...state, name: payload };
    },
    setUser(state, payload) {
        state = payload;
    },
    reset(state) {
        state = { id: null, name: null };
    },
};

export { mutations };
