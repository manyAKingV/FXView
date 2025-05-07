# FXView
This is the AI Landscape supported by Fusionx.

## Project setup
```
npm install
```

```
npm run dev
```

```
npm run build
```

要求传输md和png格式的图片，图片有尺寸要求
md文档有书写要求，且图片名称和md名称相同
md格式见exampe.md

```
名称：PyTorch
描述：是一个由Facebook开发的开源深度学习框架，主要用于机器学习和深度学习。它在科研和工业界都非常受欢迎，因其灵活性和易用性而广受赞誉，可用于智慧城市当中
成立时间：2020
网站：https://github.com/pytorch/pytorch
标签分类：AI框架、工具和库；开源基础设施；

```

```mermaid
graph LR
  A[上传公司名称到company.md] --> B[[判断是否需要爬取公司信息]]
  M[判断依据：是否已经存在公司的详细信息] --> B
  B -->|是| C[启动python脚本]
  C --> E[生成公司的md文档和公司logo]
  B -->|否| D[存入公司信息到weight.json中，并初始化当前公司的权重为10]
  D --> F[npm run build 并 部署到服务器]
  E --> D
