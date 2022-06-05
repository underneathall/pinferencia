#!/bin/bash
if [[ "$(ls -l|grep -w pyproject.toml|wc -l)" -ne 1 ]]
then
    echo "============================= Boom! ============================="
    echo "You need to run this script from the root of Pinferencia project."
    echo "============================= Ciao! ============================="
    exit 1
fi
rm -rf dist/*
poetry build
MOUNT_POINT="/opt/workspace"
CMD="cd ${MOUNT_POINT}"
CMD+=" && pip3 install dist/*.whl"
CMD+=" && pytest tests/e2e_tests"

echo $CMD
echo "============================= Start ============================="
echo "Test with Image underneathall/pinferencia:latest-devel"
echo "================================================================="
docker run --rm -it \
    -v $(pwd)/dist:$MOUNT_POINT/dist \
    -v $(pwd)/tests:$MOUNT_POINT/tests \
    underneathall/pinferencia:latest-devel bash -c "$CMD"
if [[ $? -ne 0 ]]
then
    echo "============================= Boom! ============================="
    echo "Pytest failed. Please check the stdout above."
    echo "================================================================="
    exit 1
fi
echo "================================================================="

echo "============================ Hooray! ============================"
echo "Looks good to me."
echo "============================= Ciao! ============================="
