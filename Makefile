SHELL = /bin/bash

.PHONY: all build clean serve master

all: build

build:
	mkdir -p __html__
	python3 build.py
	cp -av css img js __html__/

clean:
	rm -fr __html__/

serve: build
	cd __html__ && python3 -m http.server 8888

master: clean build
	# NB: only adds new/updated files, not removed ones
	./build.sh
