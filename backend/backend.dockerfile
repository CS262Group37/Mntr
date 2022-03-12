FROM ubuntu:20.04

# Update the system
RUN apt-get update -y 

# Install python
RUN apt-get install -y python3 python3-pip libpq-dev
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create directory
WORKDIR /opt/mntr/backend

# Install dependencies
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Install wait script to wait for db init
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

# Start backend
CMD /wait && flask run --host=0.0.0.0
