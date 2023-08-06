path = require 'path'
webpack = require 'webpack'

HtmlWebpackPlugin = require 'html-webpack-plugin'
ExtractTextPlugin = require 'extract-text-webpack-plugin'

isProduction = process.env.NODE_ENV is 'production'

cssDev = ['style-loader', 'css-loader']
cssProd = ExtractTextPlugin.extract
  fallback: 'style-loader'
  use: ['css-loader']
  publicPath: '/dist'

cssConfig = if isProduction then cssProd else cssDev

HtmlWebpackPluginConfig = new HtmlWebpackPlugin
  template: './src/index.html'
  filename: 'index.html'
  hash: true

module.exports =
  entry: './src/index.coffee'
  output:
    filename: 'index.bundle.js'
    path: path.resolve(__dirname, 'dist')
    publicPath: '/'
  resolve:
    symlinks:true
    modules: [path.resolve(__dirname, 'node_modules')]
    alias:
      libvis: path.resolve(__dirname, 'src/libvis.coffee')
  devServer:
    contentBase: path.join(__dirname, 'dist'),
    compress: true
    hot: true
    open: true
    host: 'localhost'
    historyApiFallback: true,
    headers:
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "content-type, Authorization, x-id, Content-Length, X-Requested-With",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS"
  module:
    rules: [
      {
        test: /\.coffee$/,
        use: [
          {
            loader: 'babel-loader'
            options:
              presets: ['@babel/preset-env', '@babel/preset-react'],
          }
          'coffee-loader'
        ],
        exclude: /node_modules/
      },
      {
        test: /\.styl(us)?$/,
        #exclude: /node_modules/
        use: [
          # this will apply to both plain `.scss` files
          #AND `<style lang="stylus">` blocks in `.vue` files
          'vue-style-loader',
          'style-loader','css-loader','stylus-loader']
      }
      {
        test: /\.less$/,
        use: [{
          loader: 'style-loader' ,
        }, {
          loader: 'css-loader',
        }, {
          loader: 'less-loader',
        }],
      },
      {
        test: /\.vue$/,
        #exclude: /node_modules/
        use: ['vue-loader'],
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
       {test: /\.(jpg|jpeg|png|woff|woff2|eot|ttf|svg)$/,loader: 'url-loader?limit=100000'}


    ]
  plugins: [
    HtmlWebpackPluginConfig
    new ExtractTextPlugin
      filename: 'app.css'
      disable: !isProduction
      allChunks: true
    new webpack.HotModuleReplacementPlugin()
    new webpack.NamedModulesPlugin()
  ]
