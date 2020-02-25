const path = require("path");

module.exports = [
    {
        entry: "./scripts",
        output: {
            path: path.resolve(__dirname, "./static/"),
            filename: "js/bundle.js"
        },
        devtool: "source-map",
        module: {
            rules: [
                {
                    test: /\.(js|jsx)$/,
                    exclude: /node_modules/,
                    use: ["babel-loader", "eslint-loader"]
                }
            ]
        }
    }
];
