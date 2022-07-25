import * as Api from '../../../../api/src/api/web-card';
import * as ApiModel from '../../../../api/src/api/web-card/model';
import store from '../../store';
import * as C from '../constants';

/**
 * サービス情報取得APIをコールし、Storeに企業情報を保存する
 * @param なし
 * @return なし
 */
type ErrorDetail = {
    status: number | undefined;
};

export const getServiceInfo = async (): Promise<void | ErrorDetail> => {
    try {
        const { data } = await Api.getServiceInfoApi();
        if (data.type === C.SUCCESS_RESPONSE) {
            const payload = {
                providerName: data.provider_name,
                serviceLogoUrl: data.service_logo_url,
                serviceName: data.service_name,
            };
            store.dispatch('setCorpInfoAction', { ...payload });
            return Promise.resolve();
        } else {
            return Promise.reject({ status: undefined });
        }
    } catch (errorRes) {
        const status = { status: errorRes.status };
        return Promise.reject(status);
    }
};

/**
 * カードアクセストークン発行APIをコールし、Storeにトークンを保存する
 * @param {string} cardNum - ログイン画面で入力したカード番号。
 * @param {string} pinNum - ログイン画面で入力したPIN番号。
 * @return なし
 */

export const issueAuthToken = async (
    cardNum: string,
    pinNum: string
): Promise<void | string> => {
    try {
        const requestParams: ApiModel.IssueAuthTokenApiParams = {
            card_number: cardNum,
            pin_number: pinNum,
        };
        const { data } = await Api.issueAuthTokenApi(requestParams);

        if (data.type === C.SUCCESS_RESPONSE) {
            const payload = {
                authToken: data.auth_token,
                tokenExpirationDate: data.token_expiration_date,
                refreshToken: data.refresh_token,
            };
            store.dispatch('setAuthAction', payload);
            return Promise.resolve();
        } else {
            throw new Error();
        }
    } catch (errorRes) {
        if (errorRes.status === C.STATUS_400) {
            return Promise.reject(C.NOT_EXIST_CARD_ERROR_MESSAGE);
        }
        return Promise.reject(C.OTHER_REASON_CARD_ERROR_MESSAGE);
    }
};
