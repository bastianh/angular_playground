var path = require("path");
var webpack = require("webpack");
var ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
  cache: true,
  entry: {
    app: [
      "./frontend/app.js",
      "bootstrap-sass!./bootstrap-sass.config.js"
    ],
    vendor: ["angular", "angular-ui-router"]
  },
  output: {
    path: path.join(__dirname, "backend", "static"),
    publicPath: "/static/",
    filename: "bundle.js"
  },
  module: {
    loaders: [
      {test: /\.css$/, loader: "style!css"},

      // Needed for the css-loader when [bootstrap-webpack](https://github.com/bline/bootstrap-webpack)
      // loads bootstrap's css.
      {test: /\.woff(\?v=\d+\.\d+\.\d+)?$/, loader: "url?limit=10000&minetype=application/font-woff"},
      {test: /\.woff2(\?v=\d+\.\d+\.\d+)?$/, loader: "url?limit=10000&minetype=application/font-woff"},
      {test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, loader: "url?limit=10000&minetype=application/octet-stream"},
      {test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, loader: "file"},
      {test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, loader: "url?limit=10000&minetype=image/svg+xml"},
      {
        test: /\.html$/,
        loader: "ngtemplate?relativeTo=" + (path.resolve(__dirname, './frontend')) + "/!html",
        exclude: /node_modules/
      },
      {test: /\.js$/, loader: 'ng-annotate', exclude: /node_modules/},
    ]
  },
  plugins: [
    new webpack.optimize.CommonsChunkPlugin(/* chunkName= */"vendor", /* filename= */"vendor.bundle.js"),
    new webpack.DefinePlugin({
      __DEV__: JSON.stringify(JSON.parse(process.env.BUILD_DEV || 'true')),
      __PRERELEASE__: JSON.stringify(JSON.parse(process.env.BUILD_PRERELEASE || 'false'))
    }),
    new ExtractTextPlugin("style.css")
  ],
  devServer: {
    contentBase: "static/",
    noInfo: false,
    //hot: true,
    //inline: true,
    proxy: {
      "*": "http://localhost:5000"
    }
  }
};
