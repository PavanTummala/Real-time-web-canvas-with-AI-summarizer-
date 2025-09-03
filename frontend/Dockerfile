# Stage 1: Build the React application
FROM node:18 AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json ./

# Install dependencies
# Using "npm ci" would be better if you have a package-lock.json
RUN npm install

# Copy the rest of the application's code
COPY . .

# Build the application
RUN npm run build

# Stage 2: Serve the built application from a lightweight server
FROM node:18-alpine

WORKDIR /app

# Install `serve` to run a static server
RUN npm install -g serve

# Copy the build output from the build stage
COPY --from=build /app/build .

# Expose the port `serve` will run on
EXPOSE 3000

# Command to serve the app
CMD ["serve", "-s", ".", "-l", "3000"]
