FROM node:16

# Create directory and copy files
WORKDIR /opt/mntr/frontend
COPY frontend/package.json .

# Install dependencies
RUN npm install

# Expose port
EXPOSE 3000

# Install wait script to wait for backend
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

# Start frontend
CMD /wait && npm start
