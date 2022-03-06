FROM node:16

# Create directory and copy files
WORKDIR /opt/mntr/frontend
COPY frontend/ .

# Install dependencies and build
RUN npm install && npm run build

# Expose port
EXPOSE 3000

CMD ["npm", "start"]
