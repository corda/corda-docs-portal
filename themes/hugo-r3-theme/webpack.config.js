const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = [
    {
        entry: {
            app: ["./scripts", "./styles/scss/main.js"],
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
                    use: ["babel-loader"]
                },
                {
                    test: /\.scss$/,
                    use: [
                        MiniCssExtractPlugin.loader,
                        {
                            loader: "css-loader",
                            options: {
                                sourceMap: true,
                                importLoaders: 1
                            }
                        },
                        {
                            loader: "sass-loader",
                            options: {
                                sourceMap: true,
                                sassOptions: {
                                    outputStyle: "compressed"
                                }
                            }
                        }
                    ]
                },
                {
                    test: /\.(png|jpg|gif)$/,
                    type: "asset"
                }
            ]
        },
        plugins: [
            new MiniCssExtractPlugin({
                filename: "css/main.css",
                linkType: "text/css"
            })
        ]
    }
];
