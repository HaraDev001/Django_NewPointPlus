export type Auth = {
    authToken: string;
    tokenExpirationDate: string;
    refreshToken: string;
};

export type ServiceInfo = {
    providerName: string;
    serviceLogoUrl: string;
    serviceName: string;
};
