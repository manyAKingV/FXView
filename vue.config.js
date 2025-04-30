const { defineConfig } = require('@vue/cli-service');
const path = require('path');

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src')
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
  },
  // 扩展配置（可选）
  chainWebpack(config) {
    // 添加SVG雪碧图处理（示例）
    config.module
      .rule('svg')
      .exclude.add(path.resolve(__dirname, 'src/icons'))
      .end();
    
    config.module
      .rule('icons')
      .test(/\.svg$/)
      .include.add(path.resolve(__dirname, 'src/icons'))
      .end()
      .use('svg-sprite-loader')
      .loader('svg-sprite-loader')
      .options({ symbolId: 'icon-[name]' });
  }
});