import { mount, createLocalVue, shallowMount } from '@vue/test-utils';
import Vuex from 'vuex';
import Login from '../../../src/views/Login.vue';
import { issueAuthToken } from '../../../src/domains/login';
import corpStore from '../../../src/store/modules/corp';
import authStore from '../../../src/store/modules/auth';

jest.mock('../../../src/domains/login');
const localVue = createLocalVue();
localVue.use(Vuex);
const callGetServiceInfo = jest.fn();
const issueAuthTokenMock = issueAuthToken as jest.MockedFunction<
    typeof issueAuthToken
>;

describe('views/login', () => {
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
        issueAuthTokenMock.mockClear();
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
    it('企業ロゴが存在する場合、企業ロゴが表示されて、サービス名が表示されない', () => {
        const corpState = {
            providerName: 'hogeName',
            serviceLogoUrl: 'hogePath',
            serviceName: 'hogeServiceName',
        };
        store.dispatch('setCorpInfoAction', corpState);
        const wrapper = mount(Login, {
            store,
            localVue,
            methods: { callGetServiceInfo },
        });
        expect(wrapper.contains('v-avatar')).toBe(true);
        const src = wrapper.find('v-avatar').find('img').attributes().src;
        expect(src).toBe('hogePath');
        expect(wrapper.findAll('hogeServiceName').exists()).toBe(false);
    });
    it('企業ロゴが存在しない場合、ロゴが表示されず、サービス名が表示される', () => {
        const corpState = {
            providerName: 'hogeName',
            serviceLogoUrl: '',
            serviceName: 'hogeServiceName',
        };
        store.dispatch('setCorpInfoAction', corpState);
        const wrapper = mount(Login, {
            store,
            localVue,
            methods: { callGetServiceInfo },
        });
        expect(wrapper.contains('v-avatar')).toBe(false);
        expect(wrapper.find('div').text()).toBe('hogeServiceName');
    });
    it('カード番号とPIN番号が入力されていない場合、ログインボタンが非活性', async () => {
        const wrapper = mount(Login, {
            store,
            localVue,
            methods: { callGetServiceInfo },
        });
        await wrapper.setData({
            'form.card.number': '',
            'form.pin.number': '',
        });
        expect(wrapper.find('v-btn').attributes().disabled).toBe('true');
    });
    it('カード番号とPIN番号が入力されている場合、ログインボタンが活性', async () => {
        const wrapper = mount(Login, {
            store,
            localVue,
            methods: { callGetServiceInfo },
        });

        wrapper.vm.$data.form.card.number = '11111';
        wrapper.vm.$data.form.pin.number = '11111';

        wrapper.vm.$nextTick(() => {
            expect(wrapper.find('v-btn').attributes().disabled).toBe(undefined);
        });
    });
    it('PIN番号入力欄がデフォルトでマスクされている', async () => {
        const wrapper = mount(Login, {
            store,
            localVue,
            methods: { callGetServiceInfo },
        });
        await wrapper.setData({
            'form.pin.number': '12345',
        });
        expect(wrapper.findAll('v-text-field').at(1).attributes().type).toEqual(
            'password'
        );
    });
    it('PIN番号入力欄がマスク解除したらテキストで表示される', async () => {
        const wrapper = mount(Login, {
            store,
            localVue,
            methods: { callGetServiceInfo },
            data: {
                'form.pin.isMask': false,
            },
        });
        wrapper.vm.$data.form.pin.isMask = false;
        wrapper.vm.$nextTick(() => {
            expect(
                wrapper.findAll('v-text-field').at(1).attributes().type
            ).toEqual('text');
        });
    });
    it('ログインボタン押下時に、TOPに遷移する', () => {
        issueAuthTokenMock.mockReturnValue(Promise.resolve());
        const wrapper = shallowMount(Login, {
            store,
            localVue,
            methods: { callGetServiceInfo },
            mocks: {
                $router: {
                    push: jest.fn(),
                },
                $route: {
                    path: '/',
                },
            },
        });
        wrapper.setData({
            form: {
                card: {
                    number: '1111',
                },
                pin: {
                    number: '2222',
                },
            },
        });
        wrapper.find('v-btn').trigger('click');
        expect(issueAuthTokenMock).toHaveBeenCalledTimes(1);
        expect(wrapper.vm.$route.path).toBe('/');
    });
});
