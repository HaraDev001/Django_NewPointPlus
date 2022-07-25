module.exports = {
    publicPath: '/',
    outputDir: '../../dist/shop',
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
