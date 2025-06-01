ARG REGISTRY=quay.io
ARG OWNER=jupyter
ARG BASE_IMAGE=$REGISTRY/$OWNER/docker-stacks-foundation
#FROM $BASE_IMAGE
FROM docker.io/jupyter/docker-stacks-foundation:python-3.11.6

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

#~~~~~~~~~~~~~~~
RUN usermod -aG sudo $NB_USER && \
    echo "$NB_USER	ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    apt update && apt upgrade -y && \
    apt install --yes --no-install-recommends mc openssh-client #sshpass# wkhtmltopdf
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

USER ${NB_UID}

WORKDIR /tmp
RUN mamba install --yes \
    'nbclassic' \
    'ipywidgets' \
    'voila' \
    'jupyter_contrib_nbextensions' \
    'jupyter_nbextensions_configurator' && \
    mamba clean --all -f -y && \
    rm -rf "/home/${NB_USER}/.cache/yarn" && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}" && \
    pip install jupyter-full-width

ENV JUPYTER_PORT=8888
ENV VOILA_PORT=8866
EXPOSE $JUPYTER_PORT $VOILA_PORT

# Configure container startup
COPY nbextensions/ /usr/local/share/jupyter/nbextensions

COPY all.start.sh nbclassic.start.sh voila.start.sh /usr/local/bin
COPY docker_healthcheck.py /etc/jupyter/
COPY edit.json notebook.json /etc/jupyter
COPY all.start.sh /usr/local/bin/start-notebook.d


# Fix permissions on /etc/jupyter as root
USER root
RUN fix-permissions /etc/jupyter/

# HEALTHCHECK documentation: https://docs.docker.com/engine/reference/builder/#healthcheck
# This healtcheck works well for `lab`, `notebook`, `nbclassic`, `server`, and `retro` jupyter commands
# https://github.com/jupyter/docker-stacks/issues/915#issuecomment-1068528799
HEALTHCHECK --interval=3s --timeout=1s --start-period=3s --retries=3 \
    CMD /etc/jupyter/docker_healthcheck.py || exit 1

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}

WORKDIR "${HOME}"
