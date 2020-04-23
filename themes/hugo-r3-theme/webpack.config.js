const path = require("path");

module.exports = [{
    entry: {
        app: ["./scripts", "./styles/scss/main.scss"],
        vendor: "./scripts/vendor"
    },
    output: {
        path: path.resolve(__dirname, "./static/"),
        filename: "js/[name].js"
    },
    devtool: "source-map",
    module: {
        rules: [{
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: ["babel-loader", "eslint-loader"]
            },
            {
                test: /\.scss$/,
                use: [{
                        loader: "file-loader",
                        options: {
                            name: "css/[name].css"
                        }
                    },
                    "extract-loader",
                    {
                        loader: "css-loader",
                        options: {
                            url: false
                        }
                    },
                    "sass-loader"
                ]
            },
            {
                test: /\.(png|jpg|gif)$/,
                use: [{
                    loader: "url-loader",
                    options: {
                        limit: 5000
                    }
                }]
            }
        ]
    }
}];
