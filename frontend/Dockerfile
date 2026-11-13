FROM node:24-alpine AS build

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./
ARG VITE_API_URL=/api/v1
ARG VITE_USE_MOCKS=false
ENV VITE_API_URL=$VITE_API_URL \
    VITE_USE_MOCKS=$VITE_USE_MOCKS
RUN npm run build

FROM nginx:1.27-alpine

ENV API_HOST=salud-api-prod \
    API_SCHEME=https \
    NGINX_ENTRYPOINT_LOCAL_RESOLVERS=1
COPY frontend/nginx/default.conf /etc/nginx/templates/default.conf.template
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
