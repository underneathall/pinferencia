#!/bin/bash
Help()
{
   echo "Script to test against pypi pinferencia version"
   echo
   echo "Syntax: [-h,--help|--version]"
   echo "options:"
   echo "-h,--help     Print this Help."
   echo "--version     Version to test."
   echo
}

VERSION=
while true; do
  case "$1" in
    -h | --help ) Help; exit ;;
    --version ) VERSION="$2"; shift 2;;
    -- ) shift; break ;;
    * ) break ;;
  esac
done

if [ "${VERSION}" == "" ];
then
    echo "Target Pinferencia version not provided."
    echo ""
    Help
    exit 1
fi

if [[ "$(ls -l|grep -w pyproject.toml|wc -l)" -ne 1 ]];
then
    echo "============================= Boom! ============================="
    echo "You need to run this script from the root of Pinferencia project."
    echo "============================= Ciao! ============================="
    exit 1
fi

echo "============================= Test =============================="
echo "Target:   pinferencia[streamlit]==${VERSION}"
echo "Image:    mcr.microsoft.com/playwright/python:v1.22.0-focal"
echo "================================================================="

MOUNT_POINT="/opt/workspace"
CMD="cd ${MOUNT_POINT}"
CMD+=" && apt update && apt install -y python3-pip"
CMD+=" && pip3 install pytest"
CMD+=" && pip3 install pinferencia==${VERSION}"
CMD+=" && echo \"streamlit version: \$(pip3 freeze|grep streamlit)\""
CMD+=" && if [[ \"\$(pip3 freeze|grep streamlit|wc -l)\" -ne 0 ]]; then exit 1; fi"
CMD+=" && pytest tests/api_tests"
CMD+=" && pip3 uninstall -y pinferencia"
CMD+=" && pip3 install \"pinferencia[streamlit]==${VERSION}\""
CMD+=" && pytest tests/api_tests tests/e2e_tests"

echo $CMD
echo ""

docker run --rm -it \
    -v $(pwd)/dist:$MOUNT_POINT/dist \
    -v $(pwd)/tests:$MOUNT_POINT/tests \
    mcr.microsoft.com/playwright/python:v1.22.0-focal bash -c "$CMD"
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
