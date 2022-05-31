#!/bin/bash
. /opt/conda/etc/profile.d/conda.sh && \
    conda activate base && \
    pinfer --frontend-host=0.0.0.0 demo_app:service
