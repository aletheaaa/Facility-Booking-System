# Use the official Node.js 14 image as the parent image
FROM node:14

# Set the working directory to /app
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the application code to the container
COPY . .

# Expose port 3000
EXPOSE 3000

# Start the application
CMD ["node", "notification.js"]

#To build docker file
#docker build -t notif .

#To run docker file
#docker run -p 3000:3000 --name notif-container notif
