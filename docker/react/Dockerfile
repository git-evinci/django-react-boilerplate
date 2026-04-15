# docker/react/Dockerfile
FROM node:22.22.2-alpine3.18

RUN apk update && apk upgrade --no-cache

# Force the NPM version to match local version
RUN npm install -g npm@11.12.1

WORKDIR /app/frontend

# Copy package files
COPY ./frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy frontend source
COPY ./frontend .

# Expose Vite's default port
EXPOSE 5173

# Start the Vite development server
CMD ["npm", "run", "dev", "--", "--host"]
