#!/usr/bin/env bash

docker run --rm -dp 5316:5316 -v ${PWD}/corpora:/app/ud-annotatrix/corpora \
    --name ud-annotatrix ud-annotatrix \
    && echo "Server running! Visit http://localhost:5316" \
    && echo "Run 'docker stop ud-annotatrix' to shutdown the container"
