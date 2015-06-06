var path = require("path");
var webpack = require("webpack");
var ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
  cache: true,
  entry: {
    app: [
      "./frontend/app.js"
    ],
    vendor: ["angular", "angular-ui-router", "angular-bootstrap", "jquery", "bootstrap-sass!./bootstrap-sass.config.js"]
  },
  output: {
    path: path.join(__dirname, "backend", "static"),
    publicPath: "/static/",
    filename: "bundle.js"
  },
  module: {
    loaders: [
      {test: /\.css$/, loader: "style!css"},

      // **IMPORTANT** This is needed so that each bootstrap js file required by
      // bootstrap-webpack has access to the jQuery object
      {test: /bootstrap.*\.js$/, loader: 'imports?jQuery=jquery'},

      // Needed for the css-loader when [bootstrap-webpack](https://github.com/bline/bootstrap-webpack)
      // loads bootstrap's css.
      {test: /\.woff(\?v=\d+\.\d+\.\d+)?$/, loader: "url?limit=10000&minetype=application/font-woff"},
      {test: /\.woff2(\?v=\d+\.\d+\.\d+)?$/, loader: "url?limit=10000&minetype=application/font-woff"},
      {test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, loader: "url?limit=10000&minetype=application/octet-stream"},
      {test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, loader: "file"},
      {test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, loader: "url?limit=10000&minetype=image/svg+xml"},
      //{
      //  test: /\.tmpl$/,
      //  loader: "ngtemplate?relativeTo=" + (path.resolve(__dirname, './frontend')) + "/!html",
      //  exclude: /node_modules/
      //},
      {test: /\.html$/, loader: 'raw', exclude: /node_modules/},
      {test: /\.js$/, loader: 'ng-annotate!babel', exclude: /node_modules/},
      {test: /\.scss$/, loader: 'style!css!sass', exclude: /node_modules/},
    ]
  },
  plugins: [
    new webpack.optimize.CommonsChunkPlugin(/* chunkName= */"vendor", /* filename= */"vendor.bundle.js"),
    new webpack.DefinePlugin({
      __DEV__: JSON.stringify(JSON.stringify(process.env.NODE_ENV))
    }),
    new ExtractTextPlugin("style.css")
  ],
  devServer: {
    contentBase: "static/",
    noInfo: false,
    host: "192.168.33.12",
    //hot: true,
    //inline: true,
    proxy: {
      "*": "http://localhost:5000"
    }
  }
};
