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
    setCorpInfoAction(ctx, payload) {
        ctx.commit('setCorpInfo', payload);
    },
};

export { actions };
