jest.mock('axios');
import axios, { AxiosResponse } from 'axios';
import { createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import {
    expireAuthTokenApi,
    updateAuthTokenApi,
} from '../../../../../api/src/api/web-card';
import * as ApiModel from '../../../../../api/src/api/web-card/model';
import authStore from '../../../../src/store/modules/auth';
import * as Domain from '../../../../src/domains/common';

jest.mock('../../../../../api/src/api/web-card');
const expireAuthTokenApiMock = expireAuthTokenApi as jest.MockedFunction<
    typeof expireAuthTokenApi
>;
const updateAuthTokenApiMock = updateAuthTokenApi as jest.MockedFunction<
    typeof updateAuthTokenApi
>;
// console.log用
const spyConsoleLog = jest.spyOn(console, 'log').mockImplementation();

const expireAuthTokenSuccessResponse: AxiosResponse<ApiModel.ExpireAuthTokenApiResponse> =
    {
        status: 200,
        data: undefined,
        statusText: '',
        headers: '',
        config: {},
    };

const expireAuthTokenFailed503Response: AxiosResponse<ApiModel.ExpireAuthTokenApiResponse> =
    {
        status: 503,
        data: {
            type: 'error',
            status: {
                code: 'E9999',
                message: 'InternalServerError',
            },
        },
        statusText: '',
        headers: '',
        config: {},
    };
const expireAuthTokenFailed400Response: AxiosResponse<ApiModel.ExpireAuthTokenApiResponse> =
    {
        status: 400,
        data: {
            type: 'error',
            status: {
                code: 'E9999',
                message: 'InternalServerError',
            },
        },
        statusText: '',
        headers: '',
        config: {},
    };
const expireAuthTokenFailed403Response: AxiosResponse<ApiModel.ExpireAuthTokenApiResponse> =
    {
        status: 403,
        data: {
            type: 'error',
            status: {
                code: 'E9999',
                message: 'InternalServerError',
            },
        },
        statusText: '',
        headers: '',
        config: {},
    };

const updateAuthTokenSuccessResponse: AxiosResponse<ApiModel.UpdateAuthTokenApiResponse> =
    {
        status: 200,
        data: {
            type: 'success',
            auth_token: '認証トークン',
            token_expiration_date: '21/12/31',
            refresh_token: 'リフレッシュトークン',
        },
        statusText: '',
        headers: '',
        config: {},
    };
const updateAuthTokenFailed500Response: AxiosResponse<ApiModel.UpdateAuthTokenApiResponse> =
    {
        status: 500,
        data: {
            type: 'error',
            status: {
                code: '500',
                message: '',
            },
        },
        statusText: '',
        headers: '',
        config: {},
    };
const updateAuthTokenFailed400Response: AxiosResponse<ApiModel.UpdateAuthTokenApiResponse> =
    {
        status: 400,
        data: {
            type: 'error',
            status: {
                code: '500',
                message: '',
            },
        },
        statusText: '',
        headers: '',
        config: {},
    };
const updateAuthTokenFailed403Response: AxiosResponse<ApiModel.UpdateAuthTokenApiResponse> =
    {
        status: 403,
        data: {
            type: 'error',
            status: {
                code: '500',
                message: '',
            },
        },
        statusText: '',
        headers: '',
        config: {},
    };

const localVue = createLocalVue();
localVue.use(Vuex);

describe('domain/common', () => {
    let store: any;
    const authInitValue = {
        authToken: '',
        tokenExpirationDate: '',
        refreshToken: '',
    };
    beforeEach(() => {
        expireAuthTokenApiMock.mockClear();
        updateAuthTokenApiMock.mockClear();
        spyConsoleLog.mockClear();
        store = new Vuex.Store({
            modules: {
                auth: {
                    state: authStore.state,
                    mutations: authStore.mutations,
                    actions: authStore.actions,
                },
            },
        });
        store.dispatch('setAuthAction', authInitValue);
    });
    it('expireAuthToken(): アクセストークン失効APIのレスポンスが正常', async () => {
        const authDummyValue = {
            authToken: 'dummy',
            tokenExpirationDate: 'dummy',
            refreshToken: 'dummy',
        };
        store.dispatch('setAuthAction', authDummyValue);
        expect(store.state.auth.authToken).toEqual('dummy');
        expect(store.state.auth.tokenExpirationDate).toEqual('dummy');
        expect(store.state.auth.refreshToken).toEqual('dummy');

        expireAuthTokenApiMock.mockResolvedValue(
            expireAuthTokenSuccessResponse
        );
        await Domain.expireAuthToken();
        expect(expireAuthTokenApiMock).toHaveBeenCalledTimes(1);
        expect(store.state.auth.authToken).toEqual('');
        expect(store.state.auth.tokenExpirationDate).toEqual('');
        expect(store.state.auth.refreshToken).toEqual('');
    });
    it('expireAuthToken(): アクセストークン失効APIのレスポンスが503', async () => {
        expireAuthTokenApiMock.mockRejectedValue(
            expireAuthTokenFailed503Response
        );
        Domain.expireAuthToken();
        expect(expireAuthTokenApiMock).toHaveBeenCalledTimes(1);
        expect(store.state.auth.authToken).toEqual('');
        expect(store.state.auth.tokenExpirationDate).toEqual('');
        expect(store.state.auth.refreshToken).toEqual('');
    });
    it('expireAuthToken(): アクセストークン失効APIのレスポンスが400', async () => {
        expireAuthTokenApiMock.mockRejectedValue(
            expireAuthTokenFailed400Response
        );
        Domain.expireAuthToken();
        expect(expireAuthTokenApiMock).toHaveBeenCalledTimes(1);
        expect(store.state.auth.authToken).toEqual('');
        expect(store.state.auth.tokenExpirationDate).toEqual('');
        expect(store.state.auth.refreshToken).toEqual('');
    });
    it('expireAuthToken(): アクセストークン失効APIのレスポンスが403', async () => {
        expireAuthTokenApiMock.mockRejectedValue(
            expireAuthTokenFailed403Response
        );
        Domain.expireAuthToken();
        expect(expireAuthTokenApiMock).toHaveBeenCalledTimes(1);
        expect(store.state.auth.authToken).toEqual('');
        expect(store.state.auth.tokenExpirationDate).toEqual('');
        expect(store.state.auth.refreshToken).toEqual('');
    });
    it('updateAuthToken(): アクセストークン更新APIのレスポンスが正常', async () => {
        updateAuthTokenApiMock.mockResolvedValue(
            updateAuthTokenSuccessResponse
        );
        await Domain.updateAuthToken();
        expect(updateAuthTokenApiMock).toHaveBeenCalledTimes(1);
        expect(store.state.auth.authToken).toEqual('認証トークン');
        expect(store.state.auth.tokenExpirationDate).toEqual('21/12/31');
        expect(store.state.auth.refreshToken).toEqual('リフレッシュトークン');
    });
    it('updateAuthToken(): アクセストークン更新APIのレスポンスが500', async () => {
        updateAuthTokenApiMock.mockRejectedValue(
            updateAuthTokenFailed500Response
        );
        const result = Domain.updateAuthToken();
        expect(updateAuthTokenApiMock).toHaveBeenCalledTimes(1);
        expect(store.state.auth.authToken).toEqual('');
        expect(store.state.auth.tokenExpirationDate).toEqual('');
        expect(store.state.auth.refreshToken).toEqual('');
        expect(result).rejects.toEqual(undefined);
    });
    it('updateAuthToken(): アクセストークン更新APIのレスポンスが400', async () => {
        updateAuthTokenApiMock.mockRejectedValue(
            updateAuthTokenFailed400Response
        );
        const result = Domain.updateAuthToken();
        expect(updateAuthTokenApiMock).toHaveBeenCalledTimes(1);
        expect(store.state.auth.authToken).toEqual('');
        expect(store.state.auth.tokenExpirationDate).toEqual('');
        expect(store.state.auth.refreshToken).toEqual('');
        expect(result).rejects.toEqual(undefined);
    });
    it('updateAuthToken(): アクセストークン更新APIのレスポンスが403', async () => {
        updateAuthTokenApiMock.mockRejectedValue(
            updateAuthTokenFailed403Response
        );
        const result = Domain.updateAuthToken();
        expect(updateAuthTokenApiMock).toHaveBeenCalledTimes(1);
        expect(store.state.auth.authToken).toEqual('');
        expect(store.state.auth.tokenExpirationDate).toEqual('');
        expect(store.state.auth.refreshToken).toEqual('');
        expect(result).rejects.toEqual(undefined);
    });
});
