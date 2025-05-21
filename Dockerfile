FROM registry.cn-beijing.aliyuncs.com/acs/node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm config set registry https://registry.npmmirror.com \
    && npm ci --production --no-optional --fetch-timeout=300000
COPY . .
RUN npm run build

# 阶段2：生产环境
FROM registry.cn-beijing.aliyuncs.com/acs/nginx:alpine
RUN rm -f /etc/nginx/conf.d/default.conf \
    && chown -R nginx:nginx /var/cache/nginx
COPY nginx.conf /etc/nginx/conf.d/app.conf
COPY --from=builder --chown=nginx:nginx /app/dist /usr/share/nginx/html
USER nginx
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]