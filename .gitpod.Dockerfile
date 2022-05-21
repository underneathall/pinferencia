FROM gitpod/workspace-full:2022-05-19-00-05-18
COPY ./scripts/setup-dependencies.sh /opt/setup-dependencies.sh
WORKDIR /workspace/pinferencia
RUN /opt/setup-dependencies.sh
