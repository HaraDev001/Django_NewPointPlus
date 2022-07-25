import { mount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import Header from '../../../src/components/Header.vue';
import { expireAuthToken } from '../../../src/domains/common';
import corpStore from '../../../src/store/modules/corp';
import authStore from '../../../src/store/modules/auth';

jest.mock('../../../src/domains/common');
const localVue = createLocalVue();
localVue.use(Vuex);

const handleLogout = jest.fn();
const expireAuthTokenMock = expireAuthToken as jest.MockedFunction<
    typeof expireAuthToken
>;

describe('components/Header.vue', () => {
    let store: any;
    const corpInitValue = {
        providerName: '',
        serviceLogoUrl: '',
        serviceName: '',
    };
    const authInitValue = {
        authenticationToken: '',
    };
    beforeEach(() => {
        expireAuthTokenMock.mockClear();
        store = new Vuex.Store({
            modules: {
                corp: {
                    state: corpStore.state,
                    mutations: corpStore.mutations,
                    actions: corpStore.actions,
                    getters: corpStore.getters,
                },
                auth: {
                    state: authStore.state,
                    mutations: authStore.mutations,
                    actions: authStore.actions,
                    getters: authStore.getters,
                },
            },
        });
        store.dispatch('setCorpInfoAction', corpInitValue);
        store.dispatch('setAuthAction', authInitValue);
    });
    it('呼び出し元からisBackのpropsが渡された場合、戻るボタンを表示し、戻るボタン押下時に画面遷移する', () => {
        const wrapper = mount(Header, {
            store,
            localVue,
            mocks: {
                $router: {
                    go: jest.fn(),
                },
            },
            propsData: {
                isBack: true,
            },
        });
        const vBtn = wrapper.findAll('v-col').at(0).find('v-btn');
        expect(vBtn.find('v-icon').text()).toBe('chevron_left');
        vBtn.trigger('click');
        expect(wrapper.vm.$router.go).toHaveBeenCalledTimes(1);
    });
    it('企業名と企業ロゴが表示される', () => {
        const corpState = {
            providerName: 'hogeName',
            serviceLogoUrl: 'hogePath',
            serviceName: 'hogeServiceName',
        };
        store.dispatch('setCorpInfoAction', corpState);
        const wrapper = mount(Header, {
            store,
            localVue,
            propsData: {
                isBack: false,
            },
        });
        expect(wrapper.findAll('v-col').at(0).find('v-btn').exists()).toBe(
            false
        );
        expect(wrapper.findAll('v-col').at(0).attributes().offset).toBe('1');
        expect(wrapper.find('v-img').attributes().src).toBe('hogePath');
        expect(wrapper.findAll('v-col').at(1).find('div').text()).toBe(
            'hogeName'
        );
    });
    it('アカウントメニューが表示され、ログアウトボタンを押下するとログアウトが実行される', () => {
        const corpState = {
            providerName: 'hogeName',
            serviceLogoUrl: 'hogePath',
            serviceName: 'hogeServiceName',
        };
        store.dispatch('setCorpInfoAction', corpState);

        expireAuthTokenMock.mockResolvedValue();
        const wrapper = mount(Header, {
            store,
            localVue,
            methods: { handleLogout },
            propsData: {
                isBack: false,
            },
        });
        expect(wrapper.find('v-menu').exists()).toBe(true);
        wrapper.find('v-list-item-title').trigger('click');
        expect(handleLogout).toHaveBeenCalledTimes(1);
    });
});
