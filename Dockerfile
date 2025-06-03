# 使用轻量级 Nginx 基础镜像
FROM nginx:alpine
RUN rm -rf /etc/nginx/conf.d/default.conf
COPY build/ /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/

# 暴露 80 端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]