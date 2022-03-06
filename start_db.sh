#!/bin/bash

docker run -d --env-file backend/.env -p 5432:5432 --name mntr_database postgres