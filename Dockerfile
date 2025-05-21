
# 阶段1：构建环境（使用官方LTS版本）
FROM node:18-alpine AS builder
WORKDIR /app

# 优先复制依赖文件以利用缓存
COPY package.json package-lock.json ./
RUN npm ci --production --no-optional

# 复制源码并构建
COPY . .
RUN npm run build

FROM nginx:alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/
# 直接使用 GitHub Actions 构建的 dist 目录
COPY /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]