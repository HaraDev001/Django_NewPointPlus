process.env.VUE_CLI_BABEL_TARGET_NODE = true;
process.env.VUE_CLI_BABEL_TRANSPILE_MODULES = true;

module.exports = {
    preset: '@vue/cli-plugin-unit-jest/presets/typescript-and-babel',
    setupFiles: ['jest-localstorage-mock'],
    verbose: true,
};
