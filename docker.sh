#!/usr/bin/env bash

# remove existing container if it exists
if [ "$(docker ps -aq -f name=kestra)" ]; then
    docker rm -vf kestra
fi

docker run \
  --pull=always --rm -it \
  --name kestra \
  -p 8080:8080 \
  --user=root \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd)/data/tmp:/tmp \
  kestra/kestra:latest server local
