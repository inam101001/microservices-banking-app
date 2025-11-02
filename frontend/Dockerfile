
    FROM node:20 AS build
    WORKDIR /app
    
    # COPY package.json files from frontend folder
    COPY frontend/package*.json ./
    RUN npm install
    
    # COPY frontend source code
    COPY frontend/ ./
    
    # build the React app
    RUN npm run build
    
    # --- runtime stage ---
    FROM nginx:alpine
    
    # copy React build
    COPY --from=build /app/build /usr/share/nginx/html
    
    # copy nginx config
    COPY k8s/manifests/frontend/nginx.conf /etc/nginx/conf.d/default.conf
    