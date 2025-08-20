all: opus 

users: 
	uv run ./generate-users.py 

opus: users
	ansible-playbook -i inventory.yaml base.yaml 

userclean:
	for user in $$(grep cis90 /etc/passwd | cut -d: -f1); do sudo userdel -f -r $$user; done

clean:
	-rm -rf users/

.PHONY: users opus clean userclean