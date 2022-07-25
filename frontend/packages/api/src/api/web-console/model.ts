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
    status?: {
        code: string;
        message: string;
    };
};

export type GetServiceInfoApiResponse =
    | (CommonSuccessResponse)
    | CommonErrorResponse;

export type IssueAuthTokenApiParams = {
    email: string,
    login_password: string,
    send_email_flag: number
};

type IssueAuthTokenApiSuccessResponse = {
    token: string;
    token_expiration_date: string;
    refresh_token: string;
};

export type IssueAuthTokenApiResponse =
    | (IssueAuthTokenApiSuccessResponse & CommonSuccessResponse)
    | CommonErrorResponse;

export type ExpireAuthTokenApiParams = {
    refresh_token: string;
};

export type ExpireAuthTokenApiResponse = void | CommonErrorResponse;

export type UpdateAuthTokenApiParams = {
    refresh_token: string;
};

type UpdateAuthTokenApiSuccessResponse = {
    token: string;
    token_expiration_date: string;
    terms_of_service_disagreement_flag: boolean;
    refresh_token?: string;
};

export type UpdateAuthTokenApiResponse =
    | (UpdateAuthTokenApiSuccessResponse & CommonSuccessResponse)
    | CommonErrorResponse;
