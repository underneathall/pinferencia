#!/bin/bash
python main.py --save-model --epochs=1 \
&& python prepare.py \
&& python test.py
