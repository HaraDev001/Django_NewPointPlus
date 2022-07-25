// 共通エラーレスポンス
// type: 'error'や'success'は、domain側でunion型を判別するために定義している
type CommonErrorResponse = {
    type: 'error';
    status: {
        code: string;
        message: string;
    };
};

// 共通正常レスポンス
type CommonSuccessResponse = {
    type: 'success';
};

// サービス情報取得API
type GetServiceInfoApiSuccessResponse = {
    provider_name: string;
    service_name: string;
    service_logo_url: string;
    use_service: {
        is_physical_card_enable: boolean;
    };
    use_account: {
        is_value_enable: boolean;
        is_payable_bonus_enable: boolean;
        is_exchange_bonus_enable: boolean;
    };
    terms_of_service: {
        url: string;
        regulation_date: string;
        version: string;
    };
    privacy_policy: {
        url: string;
        regulation_date: string;
        version: string;
    };
};

export type GetServiceInfoApiResponse =
    | (GetServiceInfoApiSuccessResponse & CommonSuccessResponse)
    | CommonErrorResponse;

// カードアクセストークン発行API
export type IssueAuthTokenApiParams = {
    card_number: string;
    pin_number: string;
};

type IssueAuthTokenApiSuccessResponse = {
    auth_token: string;
    token_expiration_date: string;
    refresh_token: string;
};

export type IssueAuthTokenApiResponse =
    | (IssueAuthTokenApiSuccessResponse & CommonSuccessResponse)
    | CommonErrorResponse;

// カードアクセストークン失効API
export type ExpireAuthTokenApiParams = {
    refresh_token: string;
};

export type ExpireAuthTokenApiResponse = void | CommonErrorResponse;

// カードアクセストークン更新API
export type UpdateAuthTokenApiParams = {
    refresh_token: string;
};

type UpdateAuthTokenApiSuccessResponse = {
    auth_token: string;
    token_expiration_date: string;
    refresh_token: string;
};

export type UpdateAuthTokenApiResponse =
    | (UpdateAuthTokenApiSuccessResponse & CommonSuccessResponse)
    | CommonErrorResponse;
