// ./webpack.config.babel.js
import path from "path";

export default {
  entry: {
    firstpost: ["./app/first-post.js"],
    // js bundle for other posts, e.g.
    // secondpost: ["./app/second-post.js"]
  },
  output: {
    path: path.resolve(__dirname, "static", "js"),
    filename: "[name].bundle.js"
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        use: ['babel-loader'],
        exclude: /node_modules/
      }
    ]
  }
};
