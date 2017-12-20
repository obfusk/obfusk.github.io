SHELL := /bin/bash
PY    := python3
ME    := obfusk

.PHONY: build clean serve master

build: css/pygments.css data/gists.json data/repos.json
	mkdir -p __html__
	$(PY) build.py
	cp -av css img js __html__/

css/pygments.css:
	pygmentize -S friendly -f html -a .codehilite > $@

data/gists.json: data/gh-gists.json
	# TODO

data/repos.json: data/gh-repos.json
	./data/repos.py

data/gh-gists.json:
	$(PY) -m data.gh gists $(ME) > $@

data/gh-repos.json:
	$(PY) -m data.gh repos $(ME) > $@

clean:
	find -name '*~' -delete -print
	rm -fr __html__/
	rm -f css/pygments.css
	find -name '*.pyc' -delete
	find -name __pycache__ -delete

serve: build
	cd __html__ && $(PY) -m http.server 8888

master: clean build
	./build.sh
