FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt install -y \
    curl python3 python3-pip \
    python3-opencv python3-dev && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

RUN curl -o ~/miniconda.sh \
    -O https://repo.anaconda.com/miniconda/Miniconda3-latest-$(uname -s)-$(uname -m).sh && \
    chmod +x ~/miniconda.sh && \
    ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    /opt/conda/bin/conda clean -ya

RUN . /opt/conda/etc/profile.d/conda.sh && \
    conda activate base && \
    conda install -y pytorch cpuonly -c pytorch && \
    conda install -y torchvision && \
    pip install --no-cache-dir transformers scipy && \
    pip install --no-cache-dir pytorch-pretrained-biggan && \
    /opt/conda/bin/conda clean -ya

COPY . /opt/pinferencia
RUN . /opt/conda/etc/profile.d/conda.sh && \
    conda activate base && \
    pip install --no-cache-dir poetry && \
    cd /opt/pinferencia &&\
    poetry install && \
    poetry build && \
    pip install --no-cache-dir /opt/pinferencia/dist/*.whl && \
    conda install psutil && \
    pip install --no-cache-dir streamlit && \
    rm -rf ~/.cache/pypoetry ~/.cache/pip && \
    /opt/conda/bin/conda clean -ya

COPY examples/demo/demo_app.py /opt/workspace/demo_app.py
COPY examples/demo/start.sh /opt/workspace/start.sh
WORKDIR /opt/workspace
RUN chmod +x start.sh
CMD ["bash", "-c", "./start.sh"]
