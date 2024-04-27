#!/bin/bash

docker build -t scoringbot .
docker run --rm -it --network=host scoringbot
