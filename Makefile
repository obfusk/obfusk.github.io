SHELL     := /bin/bash
PY        := python3
ME        := obfusk

HTMLROOT  ?= __html__

CSSV      := https://jigsaw.w3.org/css-validator/validator
CSSOK     := Congratulations! No Error Found.

HTMLV     := https://html5.validator.nu
HTMLOK    := The document is valid HTML5

H5VCMD    := html5validator --show-warnings --log INFO --no-langdetect

.PHONY: build clean serve master validate validate-css validate-html \
        ci-test

build: css/pygments.css data/repos.json data/gists.json \
       data/contribs.json
	mkdir -p __html__
	$(PY) build.py
	cp -av -t __html__ css img js .travis.yml

css/pygments.css:
	pygmentize -S friendly -f html -a .codehilite > $@

data/repos.json: data/gh-repos.json data/repos-blacklist.json \
                 data/repos-cats.json data/repos-tags.json
	$(PY) -m data.repos

data/gists.json: data/gh-gists.json
	# TODO

data/contribs.json: data/gh-contribs.json data/gh-contribs-add.json \
                    data/contribs-blacklist.json
	$(PY) -m data.contribs

data/gh-repos.json:
	$(PY) -m data.gh repos $(ME) > $@

data/gh-gists.json:
	$(PY) -m data.gh gists $(ME) > $@

data/gh-contribs.json:
	$(PY) -m data.gh contribs $(ME) > $@

clean:
	find -name '*~' -delete -print
	rm -fr __html__/
	rm -f css/pygments.css
	find -name '*.pyc' -delete
	find -name __pycache__ -delete

serve: build
	cd __html__ && $(PY) -m http.server 8888

master: clean build
	./build-master.sh

validate: validate-css validate-html

validate-css:
	[ $(HTMLROOT) != __html__ ] || make build
	for file in $(HTMLROOT)/css/*.css; do \
	  echo "$$file" | grep -q bootstrap && continue; \
	  echo "validating $$file..."; \
	  curl -sF "file=@$$file;type=text/css" -- "$(CSSV)" \
	    | grep -qF '$(CSSOK)' || exit 1; \
	done

validate-html:
	[ $(HTMLROOT) != __html__ ] || make build
	for file in $$( find $(HTMLROOT) -name '*.html' | sort ); do \
	  echo "validating $$file..."; \
	  curl -sF "file=@$$file;type=text/html" -- "$(HTMLV)" \
	    | grep -qF '$(HTMLOK)' || exit 1; \
	done

ci-test: validate-css
	$(H5VCMD) --root $(HTMLROOT)/ --blacklist old
