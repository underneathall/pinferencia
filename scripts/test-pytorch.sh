#!/bin/bash
if [[ "$(ls -l|grep -w pyproject.toml|wc -l)" -ne 1 ]]
then
    echo "============================= Boom! ============================="
    echo "You need to run this script from the root of Pinferencia project."
    echo "============================= Ciao! ============================="
    exit 1
fi

TEST_DIR="/tests/extra/pytorch"
MOUNT_POINT="/opt/workspace"
CMD="cd ${MOUNT_POINT}/mnist "
CMD+="&& /bin/bash test.sh"

docker run --rm -it -v "$(pwd)$TEST_DIR":$MOUNT_POINT pytorch/pytorch:latest bash -c "$CMD"
