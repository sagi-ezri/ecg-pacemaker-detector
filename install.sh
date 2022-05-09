#!/bin/sh
python3 -m pip install wfdb
pip install matplotlib==3.1.3
pip install neurokit2
poetry install
poetry show -v >.tmp_poetry
export pythonPath=$(grep -r "virtualenv" .tmp_poetry | sed 's/.*: //1')
rm .tmp_poetry
cat .vscode/settings_template.json | sed "s|\"python.pythonPath\": \".*\"|\"python.pythonPath\": \"$pythonPath/bin/python\"|1" >.vscode/settings.json

export pyenvcfg="$pythonPath/pyvenv.cfg"
echo "$(cat $pyenvcfg | sed -e 's/\(include-system-site-packages =\) false/\1 true/1')" >$pyenvcfg
