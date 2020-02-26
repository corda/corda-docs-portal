const path = require("path");

module.exports = [
    {
        entry: {
            app: "./scripts",
            vendor: "./scripts/vendor"
        },
        output: {
            path: path.resolve(__dirname, "./static/"),
            filename: "js/[name].js"
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
