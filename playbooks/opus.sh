#! /bin/bash 

ansible-playbook --connection=local --inventory=127.0.0.1, --limit 127.0.0.1 base.yaml 
ansible-playbook --connection=local --inventory=127.0.0.1, --limit 127.0.0.1 labs.yaml 

python3 ./generate-users.py cis90 29308 > users-data.yaml 
ansible-playbook --connection=local --inventory=127.0.0.1, --limit 127.0.0.1 users.yaml 
