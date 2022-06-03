FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

COPY requirements.txt /opt/requirements.txt

RUN apt-get update && apt install -y \
    curl python3 python3-pip python3-dev gcc && \
    pip3 install --no-cache-dir pytest playwright streamlit && \
    pip3 install --no-cache-dir -r /opt/requirements.txt && \
    playwright install && playwright install-deps && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean
