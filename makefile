
all: local

local: 
	python3 ./generate-users.py cis90 29308 > users/users.yaml
	ansible-playbook --connection=local --inventory=127.0.0.1, --limit 127.0.0.1 users.yaml 

clean:
	# Remove all generated users 
	for user in $(shell grep cis90 /etc/group | cut -d: -f4 | tr , ' '); do sudo deluser --remove-home $$user; done
