# ------- STAGE 1 : Build Angular -------
FROM node:20-alpine AS build

WORKDIR /app

# Copier les définitions de dépendances
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier tout le projet
COPY . .

# Builder Angular en mode production
RUN npm run build --prod

# ------- STAGE 2 : Serveur Nginx -------
FROM nginx:alpine

# Copier les fichiers buildés dans Nginx
COPY --from=build /app/dist/front /usr/share/nginx/html

# Remplacer la conf Nginx par la tienne
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
