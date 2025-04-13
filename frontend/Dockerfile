# --- Stage 1: Build Stage ---
    FROM node:23-alpine AS builder
    WORKDIR /app
    COPY . .
    RUN npm install --frozen-lockfile
    COPY . .
    RUN npm run build
    
    # --- Stage 2: Production Stage ---
    FROM node:23-alpine
    WORKDIR /app
    COPY --from=builder /app/public ./public
    COPY --from=builder /app/.next/standalone ./
    COPY --from=builder /app/.next/static ./.next/static
    EXPOSE 3000
    CMD ["node", "server.js"]