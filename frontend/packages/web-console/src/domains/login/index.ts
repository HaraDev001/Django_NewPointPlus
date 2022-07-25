import * as Api from '../../../../api/src/api/web-console';
import * as ApiModel from '../../../../api/src/api/web-console/model';
import store from '../../store';
import * as C from '../../domains/constants';

/**
 * コンソールアクセストークン発行APIをコールし、Storeにトークンを保存する
 * @param {string} email - ログイン画面で入力したメール。
 * @param {string} loginPassword - ログイン画面で入力したログインパスワード。
 * @param {string} sendEmailFlag - ログイン画面で入力したメールフラグを送信する。
 * @return なし
 */

export const issueAuthToken = async (
    email: string,
    loginPassword: string,
    sendEmailFlag: number
): Promise<void | string> => {
    try {
        const requestParams: ApiModel.IssueAuthTokenApiParams = {
            email: email,
            login_password: loginPassword,
            send_email_flag: sendEmailFlag,
        };
        const { data } = await Api.issueAuthTokenApi(requestParams);

        // check login success
        if (!data.status) {
            if (data.type === C.SUCCESS_RESPONSE) {
                const payload = {
                    authToken: data.token,
                    tokenExpirationDate: data.token_expiration_date,
                    refreshToken: data.refresh_token,
                };
                store.dispatch('setAuthAction', payload);
                return Promise.resolve();
            }
        }
        // check login and else
        else if (data.status) {
            return Promise.reject(data.status.message);
        } else {
            throw new Error();
        }
    } catch (errorRes) {
        if (errorRes.data.status) {
            return Promise.reject(errorRes.data.status.message);
        }
        if (errorRes.status === C.STATUS_400) {
            return Promise.reject(C.NOT_EXIST_ACCOUNT_ERROR_MESSAGE);
        }
        return Promise.reject(C.OTHER_REASON_ACCOUNT_ERROR_MESSAGE);
    }
};
