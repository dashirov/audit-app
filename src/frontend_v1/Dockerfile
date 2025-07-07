# Stage 1: Build the frontend
FROM node:20-alpine AS build

WORKDIR /app

COPY  index.tsx .
COPY  vite.config.js .
COPY  package.json .
COPY  img img

RUN tree -a . | head

RUN npm install

RUN npm run

EXPOSE 5173

# Stage 2: Serve the frontend using a simple static server
#FROM nginx:alpine
#COPY --from=build /app/dist /usr/share/nginx/html
#EXPOSE 80
#CMD ["nginx", "-g", "daemon off;"]