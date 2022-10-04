#! /bin/bash 

test_playbook="$1"

ansible-playbook --connection=local --inventory=127.0.0.1, --limit 127.0.0.1 base.yaml 

python3 -m venv venv 
. ./venv/bin/activate 
pip3 install -e ../libs
python3 ./generate-users.py > users-data.yaml 
ansible-playbook --connection=local --inventory=127.0.0.1, --limit 127.0.0.1 test-users.yaml 

# Extras 
ansible-playbook --connection=local --inventory=127.0.0.1, --limit 127.0.0.1 test-extra-users.yaml 

# Setup tests.
ansible-playbook --connection=local --inventory=127.0.0.1, --limit 127.0.0.1 "$test_playbook"
