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
    asyncSetUser(ctx, payload) {
        ctx.commit('setId', payload.id!);
        ctx.commit('setName', payload.name!);
    },
    asyncReset(ctx) {
        ctx.commit('reset');
    },
};

export { actions };
