import { ServiceInfo } from '../../types';

type StateInterface = ServiceInfo;

interface GettersInterface {
    providerName: string;
    serviceLogoUrl: string;
    serviceName: string;
}

interface RootGettersInterface {
    'corp/providerName': GettersInterface['providerName'];
    'corp/serviceLogoUrl': GettersInterface['serviceLogoUrl'];
    'corp/serviceName': GettersInterface['serviceName'];
}

interface MutationsInterface {
    setCorpInfo: ServiceInfo;
}

interface RootMutationsInterface {
    'corp/setCorpInfo': MutationsInterface['setCorpInfo'];
}

interface ActionsInterface {
    setCorpInfoAction: ServiceInfo;
}

interface RootActionsInterface {
    'corp/setCorpInfoAction': ActionsInterface['setCorpInfoAction'];
}

export {
    ServiceInfo,
    StateInterface,
    GettersInterface,
    RootGettersInterface,
    MutationsInterface,
    RootMutationsInterface,
    ActionsInterface,
    RootActionsInterface,
};
