// vetur.config.js
/** @type {import('vls').VeturConfig} */
module.exports = {
    settings: {
        'vetur.useWorkspaceDependencies': true,
        'vetur.experimental.templateInterpolationService': true,
    },
    projects: [
        './frontend/packages/common-components',
        './frontend/packages/web-console',
        './frontend/packages/web-card',
        './frontend/packages/web-mypage',
        './frontend/packages/web-shop',
        // TODO: 下の書き方のほうが各項目を明示的に書けるが、認識しれくてないので一旦上の簡易的な指定方法を採用
        // {
        //     // 共通で利用する基底コンポーネントなど
        //     root: './frontend/packages/common-components',
        //     package: './package.json',
        //     tsconfig: './tsconfig.json',
        //     globalComponents: './src/lib-components/**/*.vue',
        // },
        // {
        //     // 管理Web
        //     root: './frontend/packages/web-console',
        //     package: './package.json',
        //     tsconfig: './tsconfig.json',
        //     globalComponents: './src/components/**/*.vue',
        // },
        // {
        //     // 電子マネーカードWeb
        //     root: './frontend/packages/web-card',
        //     package: './package.json',
        //     tsconfig: './tsconfig.json',
        //     globalComponents: './src/components/**/*.vue',
        // },
        // {
        //     // 消費者Web
        //     root: './frontend/packages/web-mypage',
        //     package: './package.json',
        //     tsconfig: './tsconfig.json',
        //     globalComponents: './src/components/**/*.vue',
        // },
        // {
        //     // 店舗Web
        //     root: './frontend/packages/web-shop',
        //     package: './package.json',
        //     tsconfig: './tsconfig.json',
        //     globalComponents: './src/components/**/*.vue',
        // },
    ],
};
