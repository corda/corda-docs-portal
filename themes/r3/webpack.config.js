const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = [
    {
        entry: {
            app: ["./scripts", "./styles/scss/main.scss"],
            vendor: "./scripts/vendor"
        },
        output: {
            path: path.resolve(__dirname, "./static/"),
            filename: "js/[name].js"
        },
        devtool: "source-map",
        plugins: [
            new MiniCssExtractPlugin({
              filename: 'css/main.css'
            })
          ],
        module: {
            rules: [
                {
                    test: /\.(js|jsx)$/,
                    exclude: /node_modules/,
                    use: ["babel-loader", "eslint-loader"]
                },
                {
                    test: /\.(sa|sc|c)ss$/,
                    use: [
                        {
                            loader: MiniCssExtractPlugin.loader,
                            options: {
                                hmr: process.env.NODE_ENV === 'development'
                            }
                        },
                        {
                            loader: "css-loader",
                            options: {
                                url: false
                            }
                        },
                        {
                            loader: "sass-loader",
                            options: {
                                // Prefer `dart-sass`
                                implementation: require("sass")
                            }
                        }
                    ]
                },
                {
                    test: /\.(png|jpg|gif)$/,
                    use: [
                        {
                            loader: "url-loader",
                            options: {
                                limit: 8196
                            }
                        }
                    ]
                }
            ]
        }
    }
];
