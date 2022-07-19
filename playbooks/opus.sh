#! /bin/bash 

ansible-playbook --connection=local --inventory=127.0.0.1, --limit 127.0.0.1 base.yaml 
ansible-playbook --connection=local --inventory=127.0.0.1, --limit 127.0.0.1 labs.yaml 

python3 -m venv venv 
. ./venv/bin/activate 
pip3 install -e ../libs
python3 ./generate-users.py > users-data.yaml 
ansible-playbook --connection=local --inventory=127.0.0.1, --limit 127.0.0.1 users.yaml 
