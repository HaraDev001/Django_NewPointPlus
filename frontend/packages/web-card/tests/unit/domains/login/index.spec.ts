jest.mock('axios');
import axios, { AxiosResponse } from 'axios';
import { createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import {
    getServiceInfoApi,
    issueAuthTokenApi,
} from '../../../../../api/src/api/web-card';
import * as ApiModel from '../../../../../api/src/api/web-card/model';
import corpStore from '../../../../src/store/modules/corp';
import authStore from '../../../../src/store/modules/auth';
import * as Domain from '../../../../src/domains/login';
import * as Constant from '../../../../src/domains/constants';

jest.mock('../../../../../api/src/api/web-card');
const getServiceInfoApiMock = getServiceInfoApi as jest.MockedFunction<
    typeof getServiceInfoApi
>;
const issueAuthTokenApiMock = issueAuthTokenApi as jest.MockedFunction<
    typeof issueAuthTokenApi
>;
// console.log用
const spyConsoleLog = jest.spyOn(console, 'log').mockImplementation();

const getServiceInfoSuccessResponse: AxiosResponse<ApiModel.GetServiceInfoApiResponse> =
    {
        status: 200,
        data: {
            type: 'success',
            provider_name: 'corpHoge',
            service_logo_url: 'imgHoge',
            service_name: 'serviceHoge',
            use_service: {
                is_physical_card_enable: true,
            },
            use_account: {
                is_value_enable: true,
                is_payable_bonus_enable: true,
                is_exchange_bonus_enable: true,
            },
            terms_of_service: {
                url: '利用規約URL',
                regulation_date: '利用規約規定日',
                version: '利用規約バージョン',
            },
            privacy_policy: {
                url: 'プライバシーポリシーURL',
                regulation_date: 'プライバシーポリシー規定日',
                version: 'プライバシーポリシーバージョン',
            },
        },
        statusText: '',
        headers: '',
        config: {},
    };

const getServiceInfoFailed400Response: AxiosResponse<ApiModel.GetServiceInfoApiResponse> =
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
const getServiceInfoFailed503Response: AxiosResponse<ApiModel.GetServiceInfoApiResponse> =
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

const issueAuthTokenSuccessResponse: AxiosResponse<ApiModel.IssueAuthTokenApiResponse> =
    {
        status: 200,
        data: {
            type: 'success',
            auth_token: 'abc',
            token_expiration_date: '21/12/31',
            refresh_token: '123',
        },
        statusText: '',
        headers: '',
        config: {},
    };
const issueAuthTokenFailed500Response: AxiosResponse<ApiModel.IssueAuthTokenApiResponse> =
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
const issueAuthTokenFailed400Response: AxiosResponse<ApiModel.IssueAuthTokenApiResponse> =
    {
        status: 400,
        data: {
            type: 'error',
            status: {
                code: '400',
                message: '',
            },
        },
        statusText: '',
        headers: '',
        config: {},
    };
const issueAuthTokenFailed403Response: AxiosResponse<ApiModel.IssueAuthTokenApiResponse> =
    {
        status: 403,
        data: {
            type: 'error',
            status: {
                code: '400',
                message: '',
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
    const corpInitValue = {
        providerName: '',
        serviceLogoUrl: '',
        serviceName: '',
    };
    const authInitValue = {
        authToken: '',
        tokenExpirationDate: '',
        refreshToken: '',
    };
    beforeEach(() => {
        getServiceInfoApiMock.mockClear();
        issueAuthTokenApiMock.mockClear();
        spyConsoleLog.mockClear();
        store = new Vuex.Store({
            modules: {
                corp: {
                    state: corpStore.state,
                    mutations: corpStore.mutations,
                    actions: corpStore.actions,
                },
                auth: {
                    state: authStore.state,
                    mutations: authStore.mutations,
                    actions: authStore.actions,
                },
            },
        });
        store.dispatch('setCorpInfoAction', corpInitValue);
        store.dispatch('setAuthAction', authInitValue);
    });
    it('getServiceInfo(): サービス情報取得APIのレスポンスが正常', async () => {
        getServiceInfoApiMock.mockResolvedValue(getServiceInfoSuccessResponse);
        await Domain.getServiceInfo();
        expect(getServiceInfoApiMock).toHaveBeenCalledTimes(1);
        expect(store.state.corp.providerName).toEqual('corpHoge');
        expect(store.state.corp.serviceLogoUrl).toEqual('imgHoge');
        expect(store.state.corp.serviceName).toEqual('serviceHoge');
    });
    it('getServiceInfo(): サービス情報取得APIのレスポンスが503', async () => {
        getServiceInfoApiMock.mockRejectedValue(
            getServiceInfoFailed503Response
        );
        const result = Domain.getServiceInfo();
        expect(getServiceInfoApiMock).toHaveBeenCalledTimes(1);
        expect(store.state.corp.providerName).toEqual('');
        expect(store.state.corp.serviceLogoUrl).toEqual('');
        expect(store.state.corp.serviceName).toEqual('');
        expect(result).rejects.toStrictEqual({ status: 503 });
    });
    it('getServiceInfo(): サービス情報取得APIのレスポンスが400', async () => {
        getServiceInfoApiMock.mockRejectedValue(
            getServiceInfoFailed400Response
        );
        const result = Domain.getServiceInfo();
        expect(getServiceInfoApiMock).toHaveBeenCalledTimes(1);
        expect(store.state.corp.providerName).toEqual('');
        expect(store.state.corp.serviceLogoUrl).toEqual('');
        expect(store.state.corp.serviceName).toEqual('');
        expect(result).rejects.toStrictEqual({ status: 400 });
    });
    it('issueAuthToken(): カードアクセストークン発行APIのレスポンスが正常', async () => {
        issueAuthTokenApiMock.mockResolvedValue(issueAuthTokenSuccessResponse);
        const dummyParams: ApiModel.IssueAuthTokenApiParams = {
            card_number: '1111',
            pin_number: '2222',
        };
        await Domain.issueAuthToken(
            dummyParams.card_number,
            dummyParams.pin_number
        );
        expect(issueAuthTokenApiMock).toHaveBeenCalledTimes(1);
        expect(store.state.auth.authToken).toEqual('abc');
        expect(store.state.auth.tokenExpirationDate).toEqual('21/12/31');
        expect(store.state.auth.refreshToken).toEqual('123');
    });
    it('issueAuthToken(): カードアクセストークン発行APIのレスポンスが500', async () => {
        issueAuthTokenApiMock.mockRejectedValue(
            issueAuthTokenFailed500Response
        );
        const dummyParams: ApiModel.IssueAuthTokenApiParams = {
            card_number: '1111',
            pin_number: '2222',
        };
        const result = Domain.issueAuthToken(
            dummyParams.card_number,
            dummyParams.pin_number
        );
        expect(issueAuthTokenApiMock).toHaveBeenCalledTimes(1);
        expect(store.state.auth.authToken).toEqual('');
        expect(store.state.auth.tokenExpirationDate).toEqual('');
        expect(store.state.auth.refreshToken).toEqual('');
        expect(result).rejects.toBe(Constant.OTHER_REASON_CARD_ERROR_MESSAGE);
    });
    it('issueAuthToken(): カードアクセストークン発行APIのレスポンスが400', async () => {
        issueAuthTokenApiMock.mockRejectedValue(
            issueAuthTokenFailed400Response
        );
        const dummyParams: ApiModel.IssueAuthTokenApiParams = {
            card_number: '1111',
            pin_number: '2222',
        };
        const result = Domain.issueAuthToken(
            dummyParams.card_number,
            dummyParams.pin_number
        );
        expect(issueAuthTokenApiMock).toHaveBeenCalledTimes(1);
        expect(store.state.auth.authToken).toEqual('');
        expect(store.state.auth.tokenExpirationDate).toEqual('');
        expect(store.state.auth.refreshToken).toEqual('');
        expect(result).rejects.toBe(Constant.NOT_EXIST_CARD_ERROR_MESSAGE);
    });
    it('issueAuthToken(): カードアクセストークン発行APIのレスポンスが403', async () => {
        issueAuthTokenApiMock.mockRejectedValue(
            issueAuthTokenFailed403Response
        );
        const dummyParams: ApiModel.IssueAuthTokenApiParams = {
            card_number: '1111',
            pin_number: '2222',
        };
        const result = Domain.issueAuthToken(
            dummyParams.card_number,
            dummyParams.pin_number
        );
        expect(issueAuthTokenApiMock).toHaveBeenCalledTimes(1);
        expect(store.state.auth.authToken).toEqual('');
        expect(store.state.auth.tokenExpirationDate).toEqual('');
        expect(store.state.auth.refreshToken).toEqual('');
        expect(result).rejects.toBe(Constant.OTHER_REASON_CARD_ERROR_MESSAGE);
    });
});
