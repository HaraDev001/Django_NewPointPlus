import { User } from '../../../domains/types';

type StateInterface = User;

interface GettersInterface {
    id: string | null;
    name: string | null;
}

interface RootGettersInterface {
    'user/id': GettersInterface['id'];
    'user/name': GettersInterface['name'];
}

interface MutationsInterface {
    setId: string;
    setName: string;
    setUser: User;
    reset: void;
}

interface RootMutationsInterface {
    'user/setId': MutationsInterface['setId'];
    'user/setName': MutationsInterface['setName'];
    'user/setUser': MutationsInterface['setUser'];
    'user/reset': MutationsInterface['reset'];
}

interface ActionsInterface {
    asyncSetUser: User;
    asyncReset: void;
}

interface RootActionsInterface {
    'user/asyncSetUser': ActionsInterface['asyncSetUser'];
    'user/asyncReset': ActionsInterface['asyncReset'];
}

export {
    User,
    StateInterface,
    GettersInterface,
    RootGettersInterface,
    MutationsInterface,
    RootMutationsInterface,
    ActionsInterface,
    RootActionsInterface,
};
