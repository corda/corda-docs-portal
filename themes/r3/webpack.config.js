const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

// https://generatewebpackconfig.netlify.com/

module.exports = [
  {
    name: 'js',
    entry: './src/index.js',
    output: {
      path: path.resolve(__dirname, 'static'),
      filename: 'js/bundle.js'
    },
    "devtool": "source-map",
    "module": {
      "rules": [
        {
          "enforce": "pre",
          "test": /\.(js|jsx)$/,
          "exclude": /node_modules/,
          "use": {
            loader: "eslint-loader",
            options: {
              configFile: ".eslintrc.js"
            }
          }
        },
        {
          "test": /\.scss$/,
          "use": [
            MiniCssExtractPlugin.loader,
            "css-loader",
            {
              loader: 'sass-loader',
              options: {
                // Prefer `dart-sass`
                implementation: require('sass'),
              },
            }
          ]
        }
      ]
    },
    "plugins": [new MiniCssExtractPlugin({ filename: "css/[name].css" })]
  }
];
