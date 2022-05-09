FROM python:3.6-slim

ENV HOME "/root"
ENV DOCKER_SCRIPTS "$HOME/docker-scripts"
ENV PW "thesag2008"
ENV POETRY_HOME "$HOME/.poetry"
ENV PYENV_ROOT "$HOME/.pyenv"
ENV PATH "$PYENV_ROOT/bin:$POETRY_HOME/bin:$PATH"
RUN echo "root:${PW}" | chpasswd

ADD ./entrypoint.sh $DOCKER_SCRIPTS/entrypoint.sh
RUN find $DOCKER_SCRIPTS -name '*.sh' -exec chmod a+x {} +

# Prepare python project
RUN mkdir /src
COPY ./ecg_pacemaker_mini_project /src/ecg_pacemaker_mini_project
COPY ./install.sh /src/install.sh
COPY ./entrypoint.sh /src/entrypoint.sh
COPY ./poetry.lock /src/poetry.lock
COPY ./pyproject.toml /src/pyproject.toml
COPY ./model /src/model

RUN apt-get update && apt-get -y install curl
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python -u
RUN . $HOME/.poetry/env

WORKDIR /src/
RUN ./install.sh
WORKDIR /src/
RUN ./install.sh

EXPOSE 80

ENTRYPOINT $DOCKER_SCRIPTS/entrypoint.sh
