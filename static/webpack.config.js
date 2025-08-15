const path = require('path');
const fs = require('fs');
const util = require('util');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const miniCssExtractPlugin = require('mini-css-extract-plugin');

const devTemplatesFolder = path.resolve(__dirname, "sample-templates");

var config = {

    entry: './src/index.js',
    plugins: [], // defined in function below
    output: {
        filename: '[name].bundle.js',
        clean: true,
    },

    module: {
        rules: [
            {
                test: /\.css$/i,
                use: [miniCssExtractPlugin.loader, 'css-loader'],
            },
        ],
    },
};

function buildHtmlWebpackPlugin(mode) {
    console.log("In buildHtmlWebpackPlugin in mode " + mode);
    var templateParameters = {}
    const templateNames = ["breadcrumb", "content", "sidebar", "table_of_content"];
    templateNames.forEach(name => {
        if (mode === 'production') {
            templateParameters[name] = `{{ ${name}|safe }}`;
        } else if (mode === 'development') {
            templateParameters[name] = fs.readFileSync(
                path.resolve(devTemplatesFolder, `${name}.html`),
                'utf-8'
            )
        }
    }
    )
    console.log("HtmlWebpackPlugin built with templateParameters: " + util.inspect(templateParameters, {showHidden: false, depth: null, colors: true}));
    return new HtmlWebpackPlugin({
        title: 'Output Management',
        template: './src/index.html',
        templateParameters: templateParameters,
        minify: false,
    })
}

function buildPlugins(mode) {
    return [
        buildHtmlWebpackPlugin(mode),
        new miniCssExtractPlugin(),
    ]
}


module.exports = (env, argv) => {
    config.mode = argv.mode;
    config.plugins = buildPlugins(argv.mode)

    if (argv.mode === 'development') {
        config.output.path = path.resolve(__dirname, 'dist');
    }

    if (argv.mode === 'production') {
        config.output.path = path.resolve(__dirname, '../src/gitwiki/templates')
        config.output.publicPath = "{{relative_to_root}}/_mpw_static/";
    }

    return config;
};
