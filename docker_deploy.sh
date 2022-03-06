#!/bin/bash

# Build frontend and backend
docker build --file=backend/backend.dockerfile -t mntr-backend .
docker build --file=frontend/frontend.dockerfile -t mntr-frontend .

docker compose up