#!/bin/bash
if [[ "$(ls -l|grep -w pyproject.toml|wc -l)" -ne 1 ]]
then
    echo "============================= Boom! ============================="
    echo "You need to run this script from the root of Pinferencia project."
    echo "============================= Ciao! ============================="
    exit 1
fi

poetry build
MOUNT_POINT="/opt/workspace"
CMD="cd ${MOUNT_POINT}"
CMD+=" && pip install pytest pytest-cov requests poetry"
CMD+=" && poetry install"
CMD+=" && poetry run pytest"

echo $CMD
for version in "3.6.15" "3.7.13" "3.8.13" "3.9.12" "3.10.4";
do
    echo "============================= Start ============================="
    echo "Run pytest using Python ${version}"
    image="python:${version}-slim-buster"
    echo "Run pytest using Image: ${image}"
    echo "================================================================="
    docker run --rm -it -v $(pwd):$MOUNT_POINT $image bash -c "$CMD"
    if [[ $? -ne 0 ]]
    then
        echo "============================= Boom! ============================="
        echo -e "\033[0;31mPytest failed. Please check the stdout above.\033[0m"
        echo "Python: ${version}. Image: ${image}."
        echo "================================================================="
        exit 1
    fi
    echo "============================= Ciao! ============================="
done

echo "============================ Hooray! ============================"
echo "Looks good to me."
echo "============================= Ciao! ============================="
