
all: install

install: midterm-sp2020 Vagrantfile
	mkdir -p ../../../../../static/cis-191/midterm-2020
	cp Vagrantfile ../../../../../static/cis-191/midterm-2020
	cp midterm-sp2020 ../../../../../static/cis-191/midterm-2020

midterm-sp2020: midterm-sp2020.py
	armor midterm-sp2020.py
