import { Getters } from 'vuex';
import { GettersInterface, StateInterface } from './type';

const getters: Getters<StateInterface, GettersInterface> = {
    id(state) {
        return state.id;
    },
    name(state) {
        return state.name;
    },
};

export { getters };
