FROM node:20-bookworm-slim AS build

WORKDIR /app

RUN npm install -g pnpm@9

COPY apps/web-client/package.json apps/web-client/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY apps/web-client/ .

ARG VITE_API_URL=/api
ENV VITE_API_URL=${VITE_API_URL}

RUN pnpm build

FROM nginx:1.27-alpine

COPY apps/web-client/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
