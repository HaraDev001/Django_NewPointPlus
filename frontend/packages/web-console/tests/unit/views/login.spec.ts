import { createLocalVue, shallowMount, config } from '@vue/test-utils';
import Vuex from 'vuex';
import Login from '../../../src/views/Login.vue';
import { issueAuthToken } from '../../../src/domains/login';
import authStore from '../../../src/store/modules/auth';
import Vuetify from 'vuetify';

jest.mock('../../../src/domains/login');
const localVue = createLocalVue();
config.showDeprecationWarnings = false;
localVue.config.silent = true;
localVue.use(Vuex);
localVue.use(Vuetify);
const issueAuthTokenMock = issueAuthToken as jest.MockedFunction<
    typeof issueAuthToken
>;

describe('views/login', () => {
    let store: any;
    const authInitValue = {
        authenticationToken: '',
    };
    beforeEach(() => {
        issueAuthTokenMock.mockClear();
        store = new Vuex.Store({
            modules: {
                auth: {
                    state: authStore.state,
                    mutations: authStore.mutations,
                    actions: authStore.actions,
                    getters: authStore.getters,
                },
            },
        });
        store.dispatch('setAuthAction', authInitValue);
    });

    const $t = () => {
        // i18n
    };
    it('mount Login', async () => {
        issueAuthTokenMock.mockReturnValue(Promise.resolve());
        const wrapper = shallowMount(Login, {
            store,
            localVue,
            mocks: {
                $router: {
                    push: jest.fn(),
                },
                $route: {
                    path: '/',
                },
                $t,
            },
        });
        wrapper.setData({
            user: {
                email: 'aaa@gmail.com',
                login_password: '123456',
                send_email_flag: 1,
            },
            canClick: true,
        });
        const btn = wrapper.find('#login-btn');
        await btn.trigger('click');
        expect(wrapper.element).toMatchSnapshot();
    });
});
