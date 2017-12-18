SHELL := /bin/bash

.PHONY: build clean serve master

build: css/pygments.css
	mkdir -p __html__
	python3 build.py
	cp -av css img js __html__/

css/pygments.css:
	pygmentize -S friendly -f html -a .codehilite > $@

clean:
	find -name '*~' -delete -print
	rm -fr __html__/
	rm -f css/pygments.css

serve: build
	cd __html__ && python3 -m http.server 8888

master: clean build
	./build.sh
