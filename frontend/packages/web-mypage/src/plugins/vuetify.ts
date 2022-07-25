import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import ja from 'vuetify/src/locale/ja';

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        options: {
            customProperties: true,
        },
        themes: {
            light: {
                primary: '#EF6C00',
                secondary: '#424242',
                accent: '#82B1FF',
                error: '#FF5252',
                info: '#2196F3',
                success: '#4CAF50',
                warning: '#FFC107',
            },
        },
    },
    lang: {
        locales: { ja },
        current: 'ja',
    },
    icons: {
        iconfont: 'md',
    },
});
