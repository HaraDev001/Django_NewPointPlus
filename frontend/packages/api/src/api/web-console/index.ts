import axios, { AxiosRequestConfig, AxiosResponse, Method } from 'axios';
import * as Model from './model';
import * as C from './constants';

const base = C.BASE_URI;

/**
 * APIリクエストに使用するAxiosRequestConfigを作成する関数
 * @param {string} url - ベースURL以降のAPIのURL。
 * @param {Method} method - リクエストメソッド。ex: GETやPOST
 * @param {any} args - （任意）リクエストパラメータ
 * @param {string} token - （任意）リクエストヘッダにtokenを設定する必要がある場合に使用する
 * @return {AxiosRequestConfig}
 */

// paramsは、事前の型定義ができないのでanyにしている
const createRequestConfig = (
    url: string,
    method: Method,
    args?: any,
    token?: string
): AxiosRequestConfig => {
    return {
        url: base + url,
        method,
        data: args, 
        headers: {
            Accept: 'application/json',
            Authorization: token ? token : undefined,
        },
    };
};

/**
 * コンソールアクセストークン発行APIを実行する関数
 * @param {Model.IssueAuthTokenApiParams} args - ユーザーが入力したメールとパスワードとメールフラグ
 * @return {Promise<AxiosResponse<Model.IssueAuthTokenApiResponse>>} - Promise型のAPI実行結果を返却する
 */

export const issueAuthTokenApi = async (
    args: Model.IssueAuthTokenApiParams
): Promise<AxiosResponse<Model.IssueAuthTokenApiResponse>> => {
    return new Promise((resolve, reject) => {
        const requestConfig = createRequestConfig(
            C.AUTH_TOKEN_API_URI,
            C.METHOD.POST,
            args
        );
        axios(requestConfig)
            .then((res: AxiosResponse<Model.IssueAuthTokenApiResponse>) => {
                res.data.type = 'success';
                return resolve(res);
            })
            .catch((err) => {
                err.response.data.type = 'error';
                const { response } = err;
                return reject(response);
            });
    });
};

/**
 * コンソールアクセストークン失効APIを実行する関数
 * @param {Model.ExpireAuthTokenApiParams} refreshToken - リフレッシュトークン
 * @param {Model.ExpireAuthTokenApiParams} authToken - アクセストークン
 * @return {Promise<AxiosResponse<Model.ExpireAuthTokenApiResponse>>} - Promise型のAPI実行結果を返却する
 */

export const expireAuthTokenApi = async (
    refreshToken: Model.ExpireAuthTokenApiParams,
    authToken: string
): Promise<AxiosResponse<Model.ExpireAuthTokenApiResponse>> => {
    return new Promise((resolve, reject) => {
        const requestConfig = createRequestConfig(
            C.AUTH_TOKEN_API_URI,
            C.METHOD.DELETE,
            refreshToken,
            authToken
        );
        axios(requestConfig)
            .then((res: AxiosResponse<Model.ExpireAuthTokenApiResponse>) => {
                return resolve(res);
            })
            .catch((err) => {
                err.response.data.type = 'error';
                const { response } = err;
                return reject(response);
            });
    });
};

/**
 * コンソールアクセストークン更新APIを実行する関数
 * @param {Model.UpdateAuthTokenApiParams} refreshToken - リフレッシュトークン
 * @return {Promise<AxiosResponse<Model.UpdateAuthTokenApiResponse>>} - Promise型のAPI実行結果を返却する
 */

export const updateAuthTokenApi = async (
    refreshToken: Model.UpdateAuthTokenApiParams
): Promise<AxiosResponse<Model.UpdateAuthTokenApiResponse>> => {
    return new Promise((resolve, reject) => {
        const requestConfig = createRequestConfig(
            C.AUTH_TOKEN_API_URI,
            C.METHOD.PUT,
            refreshToken
        );
        axios(requestConfig)
            .then((res: AxiosResponse<Model.UpdateAuthTokenApiResponse>) => {
                res.data.type = 'success';
                return resolve(res);
            })
            .catch((err) => {
                err.response.data.type = 'error';
                const { response } = err;
                return reject(response);
            });
    });
};

