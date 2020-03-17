module.exports = {
    env: {
        browser: true,
        es6: true,
        node: true
    },
    extends: "eslint:recommended",
    globals: {
        Atomics: "readonly",
        SharedArrayBuffer: "readonly"
    },
    parser: "babel-eslint",
    parserOptions: {
        ecmaVersion: 2018,
        sourceType: "module"
    },
    rules: {
        "arrow-parens": ["error", "as-needed"],
        "comma-dangle": [2, "never"],
        "no-multiple-empty-lines": ["error", { max: 2, maxEOF: 1 }],
        "object-curly-newline": 0,
        semi: ["error", "always"]
    }
};
