jest.mock('axios');
import { AxiosResponse } from 'axios';
import { createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import {
    expireAuthTokenApi,
    updateAuthTokenApi,
} from '../../../../../api/src/api/web-console';
import * as ApiModel from '../../../../../api/src/api/web-console/model';
import authStore from '../../../../src/store/modules/auth';
import * as Domain from '../../../../src/domains/common';

jest.mock('../../../../../api/src/api/web-console');
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

const expireAuthTokenFailedResponse: AxiosResponse<ApiModel.ExpireAuthTokenApiResponse> =
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

const successApiResponse = {
    token: 'success_token',
    token_expiration_date: '2021-08-18T07:47:31.398400Z',
    refresh_token: 'success_refresh',
};
const updateAuthTokenSuccessResponse: AxiosResponse<ApiModel.UpdateAuthTokenApiResponse> =
    {
        status: 200,
        data: {
            ...successApiResponse,
            ...{ type: 'success', terms_of_service_disagreement_flag: true },
        },
        statusText: '',
        headers: '',
        config: {},
    };
const updateAuthTokenFailedResponse: AxiosResponse<ApiModel.UpdateAuthTokenApiResponse> =
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

const localVue = createLocalVue();
localVue.use(Vuex);

describe('domain/common', () => {
    let store: any;
    const authInitValue = {
        authToken: 'testauth',
        tokenExpirationDate: '2020/10/10',
        refreshToken: 'testrefresh',
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
    it('expireAuthToken(): clear token', async () => {
        const authDummyValue = {
            authToken: 'dummy',
            tokenExpirationDate: 'dummy',
            refreshToken: 'dummy',
        };
        store.dispatch('setAuthAction', authDummyValue);
        expect(localStorage.setItem).toHaveBeenLastCalledWith(
            'auth',
            JSON.stringify(authDummyValue)
        );
        expect(localStorage.__STORE__['auth']).toEqual(
            JSON.stringify(authDummyValue)
        );

        expireAuthTokenApiMock.mockResolvedValue(
            expireAuthTokenSuccessResponse
        );
        await Domain.expireAuthToken();
        expect(expireAuthTokenApiMock).toHaveBeenCalledTimes(1);
        expect(localStorage.__STORE__['auth']).toEqual(undefined);
    });
    it('expireAuthToken(): clear token fail', async () => {
        expireAuthTokenApiMock.mockRejectedValue(expireAuthTokenFailedResponse);
        await Domain.expireAuthToken().catch((e) => {
            console.log(e);
        });
        expect(expireAuthTokenApiMock).toHaveBeenCalledTimes(1);
        expect(localStorage.__STORE__['auth']).toEqual(undefined);
    });
    it('updateAuthToken(): success', async () => {
        updateAuthTokenApiMock.mockResolvedValue(
            updateAuthTokenSuccessResponse
        );
        await Domain.updateAuthToken();
        expect(updateAuthTokenApiMock).toHaveBeenCalledTimes(1);
        const authData = {
            authToken: successApiResponse.token,
            tokenExpirationDate: successApiResponse.token_expiration_date,
            refreshToken: successApiResponse.refresh_token,
        };
        expect(localStorage.setItem).toHaveBeenLastCalledWith(
            'auth',
            JSON.stringify(authData)
        );
        expect(localStorage.__STORE__['auth']).toEqual(
            JSON.stringify(authData)
        );
    });
    it('updateAuthToken(): fail', async () => {
        updateAuthTokenApiMock.mockRejectedValue(updateAuthTokenFailedResponse);
        const result = Domain.updateAuthToken();
        expect(updateAuthTokenApiMock).toHaveBeenCalledTimes(1);
        expect(localStorage.__STORE__['auth']).toEqual(
            JSON.stringify(authInitValue)
        );
        expect(result).rejects.toEqual(undefined);
    });
});
