import { mount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import Footer from '../../../src/components/Footer.vue';
import corpStore from '../../../src/store/modules/corp';

jest.mock('../../../src/domains/common');
const localVue = createLocalVue();
localVue.use(Vuex);

describe('components/Footer.vue', () => {
    let store: any;
    const corpInitValue = {
        providerName: '',
        serviceLogoUrl: '',
        serviceName: '',
    };
    beforeEach(() => {
        store = new Vuex.Store({
            modules: {
                corp: {
                    state: corpStore.state,
                    mutations: corpStore.mutations,
                    actions: corpStore.actions,
                    getters: corpStore.getters,
                },
            },
        });
        store.dispatch('setCorpInfoAction', corpInitValue);
    });
    it('呼び出し元からisBackのpropsが渡された場合、戻るボタンを表示し、戻るボタン押下時に画面遷移する', () => {
        const corpState = {
            providerName: 'hogeName',
            serviceLogoUrl: 'hogePath',
            serviceName: 'hogeServiceName',
        };
        store.dispatch('setCorpInfoAction', corpState);
        const wrapper = mount(Footer, {
            store,
            localVue,
        });
        expect(wrapper.find('v-col').text()).toBe('©️2021 hogeName');
    });
});
