
all: build

build:
	uv run pex -v --venv -c cis90 -o dist/cis90.pex .
	uv run pex -v --venv -c kroz -o dist/kroz.pex . 

install:
	cp dist/cis90.pex /usr/bin/cis90
	cp dist/kroz.pex /usr/bin/kroz 

test:
	uv run pytest --asyncio-mode auto 

clean:
	-rm -rf dist build
	-rm -rf *.krs Islands Random flag bigfile

# local: 
# 	python3 ./generate-users.py cis90 29308 > users/users.yaml
# 	ansible-playbook --connection=local --inventory=127.0.0.1, --limit 127.0.0.1 users.yaml 
# 
# clean:
# 	# Remove all generated users 
# 	for user in $(shell grep cis90 /etc/group | cut -d: -f4 | tr , ' '); do sudo deluser --remove-home $$user; done

.PHONY: test build install
