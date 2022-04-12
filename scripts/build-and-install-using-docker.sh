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
CMD+=" && pip install dist/*.whl"

echo $CMD
for version in "3.6.15" "3.7.13" "3.8.13" "3.9.12" "3.10.4";
do
    echo "============================= Start ============================="
    echo "Build and install with Python ${version}"
    image="python:${version}-slim-buster"
    echo "Build and install with Image: ${image}"
    echo "================================================================="
    docker run --rm -it -v $(pwd):$MOUNT_POINT $image bash -c "$CMD"
    if [[ $? -ne 0 ]]
    then
        echo "============================= Boom! ============================="
        echo "Pytest failed. Please check the stdout above."
        echo "Python: ${version}. Image: ${image}."
        echo "================================================================="
        exit 1
    fi
    echo "================================================================="
done

echo "============================ Hooray! ============================"
echo "Looks good to me."
echo "============================= Ciao! ============================="
