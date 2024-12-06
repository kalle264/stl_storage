FROM python:3.11.2-bullseye

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt update && apt install -y \
    sudo vim less ack-grep rsync wget curl cmake arp-scan iproute2 iw libgeos-dev graphviz graphviz-dev v4l-utils psmisc sysstat \
    libgl1-mesa-glx ffmpeg libsm6 libxext6 \
    avahi-utils iputils-ping \
    jq \
    libusb-1.0-0 libusb-1.0-0-dev \
    && rm -rf /var/lib/apt/lists/*

ARG USERNAME=stl_storage
ARG USER_UID=1000
ARG USER_GID=1000

RUN addgroup --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && usermod -a -G dialout $USERNAME \
    && usermod -a -G tty $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME

ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"

RUN python3 -m pip install --upgrade pip

WORKDIR /app
COPY requirements.txt ./

RUN --mount=type=cache,target=/home/zauberzeug/.cache/pip \
    python3 -m pip install --user -r requirements.txt


WORKDIR /app
COPY --chown=${USERNAME}:${USER_GID} stl_storage ./stl_storage/
COPY --chown=${USERNAME}:${USER_GID} *.py ./

RUN sudo setcap 'cap_net_bind_service=+ep cap_sys_nice=+ep' /usr/local/bin/python3.11

CMD python3 main.py