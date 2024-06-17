const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    entry: './src/index.js',
    output: {
        path: path.resolve(__dirname, 'static', 'bundles'),  // Correctly set the output path
        filename: '[name]-[hash].js',  // Use only the filename here
        publicPath: 'http://localhost:3000/static/bundles/',
    },
    plugins: [
        new BundleTracker({ path: __dirname, filename: 'webpack-stats.json' })  // Correctly set the path and filename
    ],
    devServer: {
        port: 3000,
        headers: { 'Access-Control-Allow-Origin': '*' },
    },
    module: {
        rules: [
        {
            test: /\.(js|jsx)$/,
            exclude: /node_modules/,
            use: {
            loader: 'babel-loader',
            },
        },
        {
            test: /\.css$/,
            use: ['style-loader', 'css-loader'],
        },
        ],
    },
    resolve: {
        extensions: ['*', '.js', '.jsx'],
    },
};
