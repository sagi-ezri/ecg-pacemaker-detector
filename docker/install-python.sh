apt-get update && apt-get install -y \
make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils \
tk-dev libffi-dev liblzma-dev python-openssl git

# install pyenv
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
cd ~/.pyenv
git checkout 1.2.27

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"

# install python
PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install $PYTHON_VERSION
pyenv global $PYTHON_VERSION
