#!/bin/sh
eval "$(pyenv init -)"
$DOCKER_SCRIPTS/entrypoint-ssh.sh

poetry run infer &

tail -f /dev/null
