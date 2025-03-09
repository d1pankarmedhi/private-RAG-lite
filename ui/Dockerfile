FROM node:20-alpine AS builder

# Enable corepack and pnpm
RUN npm install -g corepack && \
    corepack enable && \
    corepack prepare pnpm@latest --activate

WORKDIR /app/UI

# Install system dependencies for native modules
RUN apk add --no-cache git python3 make g++

# Copy package files first for better caching
COPY package.json pnpm-lock.yaml* .npmrc* ./

# Install all dependencies including devDependencies
RUN pnpm install 

# Copy source files
COPY . .

# Build the project
RUN pnpm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/UI/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
