# Use an official Node.js runtime as the base image
FROM node:14-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package.json ./

# Install dependencies
RUN npm install --production

# Copy the rest of the application code to the container
COPY . .

# Build the React app
RUN npm run build

# Set the environment variable for the port
ENV PORT 3999

# Expose the specified port
EXPOSE $PORT

# Set the command to run the application
CMD ["npm", "run", "start"]
