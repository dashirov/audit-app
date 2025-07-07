# Stage 1: Build the frontend
FROM node:20-alpine AS build

WORKDIR /app
COPY  src/frontend/ .

RUN /usr/bin/tree -a /app

RUN npm install

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
