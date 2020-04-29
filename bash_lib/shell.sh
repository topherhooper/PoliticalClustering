#!/bin/bash
set -eux
docker build -f bash_lib/Dockerfile -t bighead .
docker run --pid=host -itP --privileged --net=host -e USER=${USER} -v $(pwd):/bighead -w /bighead --rm -m 100M --cpuset-cpus='0' --cpus=1 --cpu-shares=256 -t bighead bash