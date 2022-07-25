import { Auth } from '../../../store/types';

type StateInterface = Auth;

interface GettersInterface {
    authToken: string;
    tokenExpirationDate: string;
    refreshToken: string;
    tokenExpirationDateConvertDate: Date;
}

interface RootGettersInterface {
    'auth/authToken': GettersInterface['authToken'];
    'auth/tokenExpirationDate': GettersInterface['tokenExpirationDate'];
    'auth/refreshToken': GettersInterface['refreshToken'];
    tokenExpirationDateConvertDate: GettersInterface['tokenExpirationDateConvertDate'];
}

interface MutationsInterface {
    setAuth: Auth;
    clearAuth: void;
}

interface RootMutationsInterface {
    'auth/setAuth': MutationsInterface['setAuth'];
    'auth/clearAuth': MutationsInterface['clearAuth'];
}

interface ActionsInterface {
    setAuthAction: Auth;
    clearAuthAction: void;
}

interface RootActionsInterface {
    'auth/setAuthAction': ActionsInterface['setAuthAction'];
    'auth/clearAuthAction': ActionsInterface['clearAuthAction'];
}

export {
    Auth,
    StateInterface,
    GettersInterface,
    RootGettersInterface,
    MutationsInterface,
    RootMutationsInterface,
    ActionsInterface,
    RootActionsInterface,
};
