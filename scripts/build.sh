#!/bin/bash
docker pull pklehre/niso2019-lab3
docker build -t niso3-sxc678 .
docker image prune -f