#!/bin/bash
./scripts/build.sh
for i in {1..10}
do
    echo "===== RUN $i ====="
    docker run --rm niso3-sxc678
done
