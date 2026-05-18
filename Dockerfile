FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    ccache \
    gcc-arm-none-eabi \
    libnewlib-arm-none-eabi \
    libstdc++-arm-none-eabi-newlib \
    git \
    python3 \
    python3-pip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --break-system-packages littlefs-python==0.17.1

WORKDIR /workspace

ARG MICROPYTHON_VERSION=v1.27.0
ARG PIMORONI_PICO_VERSION=v1.27.0
ARG DIR2UF2_VERSION=v0.1.0
ARG PY_DECL_VERSION=v0.0.5

# Small tools first — cheap layers, rarely change
RUN git clone --depth 1 --branch ${PY_DECL_VERSION} https://github.com/gadgetoid/py_decl.git && \
    git clone --depth 1 --branch ${DIR2UF2_VERSION} https://github.com/gadgetoid/dir2uf2.git

# Pimoroni Pico libraries (init submodules: qrcode C module + sensor drivers)
RUN git clone --depth 1 --branch ${PIMORONI_PICO_VERSION} \
    https://github.com/pimoroni/pimoroni-pico.git && \
    cd pimoroni-pico && git submodule update --init

# MicroPython source + required submodules
RUN git clone --depth 1 --branch ${MICROPYTHON_VERSION} \
    https://github.com/micropython/micropython.git

RUN cd micropython && \
    git submodule update --init lib/pico-sdk && \
    git submodule update --init lib/cyw43-driver && \
    git submodule update --init lib/lwip && \
    git submodule update --init lib/mbedtls && \
    git submodule update --init lib/micropython-lib && \
    git submodule update --init lib/tinyusb && \
    git submodule update --init lib/btstack

# Pre-build mpy-cross (bytecode compiler used at cmake configure time)
RUN make -C micropython/mpy-cross -j$(nproc)

# Expose versions for the build script
ENV MICROPYTHON_VERSION=${MICROPYTHON_VERSION}
ENV PIMORONI_PICO_VERSION=${PIMORONI_PICO_VERSION}

# Repo is mounted at /workspace/badger2040 — see docker-compose.yml
CMD ["/workspace/badger2040/scripts/docker-build.sh"]
