module.exports = {
    publicPath: '/',
    outputDir: '../../dist/mypage',
    pluginOptions: {
        i18n: {
            locale: 'ja',
            fallbackLocale: 'ja',
            localeDir: 'locales',
            enableInSFC: false,
        },
    },
    transpileDependencies: ['vuetify'],
    pwa: {
        name: 'Point+Plus管理Web',
    },
};
