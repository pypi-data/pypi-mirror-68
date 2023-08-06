path = require 'path'

module.exports =
  entry:
    libvis: './src/libvis.coffee'
  output:
    filename: 'libvis.js'
    path: path.resolve(__dirname, 'lib')
    library: 'libvis'
    libraryTarget: 'commonjs-module'
    publicPath: '/'
  resolve:
    symlinks:true
    modules: [path.resolve(__dirname, 'node_modules')]
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
