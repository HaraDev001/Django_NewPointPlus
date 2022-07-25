jest.mock('axios');
import { AxiosResponse } from 'axios';
import { createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import { issueAuthTokenApi } from '../../../../../api/src/api/web-console';
import * as ApiModel from '../../../../../api/src/api/web-console/model';
import authStore from '../../../../src/store/modules/auth';
import * as Domain from '../../../../src/domains/login';

jest.mock('../../../../../api/src/api/web-console');

const issueAuthTokenApiMock = issueAuthTokenApi as jest.MockedFunction<
    typeof issueAuthTokenApi
>;
// console.log用
const spyConsoleLog = jest.spyOn(console, 'log').mockImplementation();

const successAuthData = {
    token: 'abc',
    token_expiration_date: '21/12/31',
    refresh_token: '123',
};
const issueAuthTokenSuccessResponse: AxiosResponse<ApiModel.IssueAuthTokenApiResponse> =
    {
        status: 200,
        data: { ...successAuthData, ...{ type: 'success' } },
        statusText: '',
        headers: '',
        config: {},
    };
const issueAuthTokenFailedResponse: AxiosResponse<ApiModel.IssueAuthTokenApiResponse> =
    {
        status: 500,
        data: {
            type: 'error',
            status: {
                code: '500',
                message: 'error 500',
            },
        },
        statusText: '',
        headers: '',
        config: {},
    };
const issueAuthTokenFailed400Response: AxiosResponse<ApiModel.IssueAuthTokenApiResponse> =
    {
        status: 400,
        data: {
            type: 'error',
            status: {
                code: '400',
                message: 'error 400 message',
            },
        },
        statusText: '',
        headers: '',
        config: {},
    };

const localVue = createLocalVue();
localVue.use(Vuex);

describe('domain/login', () => {
    let store: any;
    const authInitValue = {
        authToken: '',
        tokenExpirationDate: '',
        refreshToken: '',
    };
    beforeEach(() => {
        issueAuthTokenApiMock.mockClear();
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

    it('issueAuthToken(): success case', async () => {
        issueAuthTokenApiMock.mockResolvedValue(issueAuthTokenSuccessResponse);
        const dummyParams: ApiModel.IssueAuthTokenApiParams = {
            email: 'correct_value',
            login_password: 'correct_value',
            send_email_flag: 0,
        };
        await Domain.issueAuthToken(
            dummyParams.email,
            dummyParams.login_password,
            dummyParams.send_email_flag
        );
        expect(issueAuthTokenApiMock).toHaveBeenCalledTimes(1);
        const authData = {
            authToken: successAuthData.token,
            tokenExpirationDate: successAuthData.token_expiration_date,
            refreshToken: successAuthData.refresh_token,
        };
        expect(localStorage.setItem).toHaveBeenLastCalledWith(
            'auth',
            JSON.stringify(authData)
        );
        expect(localStorage.__STORE__['auth']).toEqual(
            JSON.stringify(authData)
        );
    });
    it('issueAuthToken(): fail case', async () => {
        issueAuthTokenApiMock.mockRejectedValue(issueAuthTokenFailedResponse);
        const dummyParams: ApiModel.IssueAuthTokenApiParams = {
            email: 'wrong_value',
            login_password: 'wrong_value',
            send_email_flag: 0,
        };
        await Domain.issueAuthToken(
            dummyParams.email,
            dummyParams.login_password,
            dummyParams.send_email_flag
        ).catch((e) => {
            expect(e).toEqual('error 500');
        });
        expect(issueAuthTokenApiMock).toHaveBeenCalledTimes(1);
    });
    it('issueAuthToken(): fail 400', async () => {
        issueAuthTokenApiMock.mockRejectedValue(
            issueAuthTokenFailed400Response
        );
        const dummyParams: ApiModel.IssueAuthTokenApiParams = {
            email: 'wrong_value',
            login_password: 'wrong_value',
            send_email_flag: 0,
        };
        await Domain.issueAuthToken(
            dummyParams.email,
            dummyParams.login_password,
            dummyParams.send_email_flag
        ).catch((e) => {
            expect(e).toEqual('error 400 message');
        });
        expect(issueAuthTokenApiMock).toHaveBeenCalledTimes(1);
    });
});
