#!/bin/bash
script_dir=$(dirname "$0")

python ${script_dir}/main.py --save-model --epochs=1 \
&& python ${script_dir}/prepare.py \
&& python ${script_dir}/test.py
