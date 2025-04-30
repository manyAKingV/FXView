FROM nginx:alpine

# 清理默认配置
RUN rm /etc/nginx/conf.d/default.conf

# 复制 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/

# 直接使用 GitHub Actions 构建的 dist 目录
COPY dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]