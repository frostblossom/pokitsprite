sudo apt-get --assume-yes install python3.7-venv
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install -U pytest
pip install pytest-watch
deactivate