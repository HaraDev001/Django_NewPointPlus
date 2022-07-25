import * as Api from '../../../../api/src/api/web-card';
import * as ApiModel from '../../../../api/src/api/web-card/model';
import store from '../../store';
import * as C from '../constants';

/**
 * アクセストークン失効APIをコールし、Storeの認証情報(auth/)を削除する
 * @param なし
 * @return なし
 */

export const expireAuthToken = async (): Promise<void> => {
    const refreshToken = store.getters.refreshToken;
    const authToken = store.getters.authToken;
    await Api.expireAuthTokenApi(refreshToken, authToken);
    return store.dispatch('clearAuthAction');
};

/**
 * アクセストークン更新APIをコールし、Storeの認証情報(auth/)を更新する
 * @param なし
 * @return なし
 */

export const updateAuthToken = async (): Promise<void> => {
    try {
        const refreshToken = store.getters.refreshToken;
        const { data } = await Api.updateAuthTokenApi({
            refresh_token: refreshToken,
        });
        if (data.type === C.SUCCESS_RESPONSE) {
            const payload = {
                authToken: data.auth_token,
                tokenExpirationDate: data.token_expiration_date,
                refreshToken: data.refresh_token,
            };
            return store.dispatch('setAuthAction', payload);
        } else {
            throw new Error();
        }
    } catch (err) {
        return Promise.reject();
    }
};
