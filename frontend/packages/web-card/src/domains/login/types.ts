export type Auth = Readonly<{
    authenticationToken: string | null;
    // expireDate: string | null;
    // refreshToken: string | null;
}>;

export type ServiceInfo = Readonly<{
    serviceLogoUrl: string | null;
}>;
