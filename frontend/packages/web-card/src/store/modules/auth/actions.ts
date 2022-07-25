import { Actions } from 'vuex';
import {
    ActionsInterface,
    GettersInterface,
    MutationsInterface,
    StateInterface,
} from './type';

const actions: Actions<
    StateInterface,
    ActionsInterface,
    GettersInterface,
    MutationsInterface
> = {
    setAuthAction(ctx, payload) {
        ctx.commit('setAuth', payload);
    },
    clearAuthAction(ctx) {
        ctx.commit('clearAuth');
    },
};

export { actions };
