#!/bin/bash

set -e 

docker stop be fe || true
docker rm be fe  || true
docker rmi be fe || true

docker build -t be be/ 
docker build -t fe fe/ 

docker run -d -p 5000:5000 --name be be
docker run -d -p 80:80 --name fe fe
