module.exports = {
    env: {
        browser: true,
        es6: true,
        node: true
    },
    extends: ["eslint:recommended", "plugin:prettier/recommended"],
    globals: {
        Atomics: "readonly",
        SharedArrayBuffer: "readonly"
    },
    parser: "babel-eslint",
    parserOptions: {
        ecmaVersion: 2020,
        sourceType: "module"
    },
    rules: {
        "comma-dangle": [2, "never"],
        "no-multiple-empty-lines": ["error", { max: 2, maxEOF: 1 }],
        "object-curly-newline": 0,
        semi: ["error", "always"]
    }
};
