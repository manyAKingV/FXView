const { defineConfig } = require('@vue/cli-service');
const path = require('path');

module.exports = defineConfig({
  transpileDependencies: true,
  runtimeCompiler: true,
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src'),
        '@scrapy':path.resolve(__dirname, 'scrapy')
      }
    },
    // 新增Markdown文件解析规则
    module: {
      rules: [
        {
          test: /\.md$/,
          use: [
            {
              loader: 'html-loader',  
              options: {
                esModule: false       
              }
            },{
              loader: 'markdown-loader', 
              options: {
                pedantic: false,      
                langPrefix: 'lang-',  
                breaks: true          
              }
            }
          ]
        }
      ]
    }
  }
});