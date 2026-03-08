FROM node:24-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

# Use 'dev' instead of 'start' for hot-reloading!
CMD ["npm", "run", "dev"]