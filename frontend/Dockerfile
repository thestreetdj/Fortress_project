# frontend/Dockerfile
FROM node:20-alpine AS build
WORKDIR /app

# package.json과 lock 파일을 먼저 복사 (캐싱 효율화)
COPY package.json package-lock.json* ./

# 에러 방지를 위해 파일이 없을 경우 빈 파일이라도 생성하게 하거나, 
# 명확하게 복사되었는지 확인하는 단계입니다.
RUN npm install

COPY . .
RUN npm run build

FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]