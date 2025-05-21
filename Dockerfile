# 阶段1：构建环境
FROM registry.cn-beijing.aliyuncs.com/acs/node:18-alpine AS builder

# 工作目录
WORKDIR /app

# 安装依赖
COPY package.json package-lock.json ./
RUN npm ci --production --no-optional

# 复制源码并构建
COPY . .
RUN npm run build

# 阶段2：生产环境（使用Nginx作为静态服务器）
FROM nginx:alpine

# 删除默认配置
RUN rm /etc/nginx/conf.d/default.conf

# 复制自定义配置
COPY nginx.conf /etc/nginx/conf.d/

# 从builder阶段复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]