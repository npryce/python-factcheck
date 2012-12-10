
# Which major version of python are we using?  Set to 2 to test in Python 2
ifndef python
python=3
endif

PROJECT=$(shell python setup.py --name)
VERSION=$(shell python setup.py --version)
SRCDIR=.

ARCHITECTURE:=$(shell uname -m)
PYTHON_ENV=$(PWD)/python$(python)-$(ARCHITECTURE)
PYTHON_EXE=$(PYTHON_ENV)/bin/python
PIP=$(PYTHON_ENV)/bin/pip

TESTS=test/test_factcheck.py $(wildcard test/test_factcheck_python$(python)*.py)

.PHONY: all
all: dist

.PHONY: env
env: env-base env-libs

.PHONY: env-base
env-base:
	mkdir -p $(dir $(PYTHON_ENV))
	tools/virtualenv --python=python$(python) $(PYTHON_ENV)
	rm -f distribute-*.tar.gz

.PHONY: env-libs
env-libs:
	$(PIP) install pytest

.PHONY: env-clean
env-clean:
	rm -rf $(PYTHON_ENV)/

.PHONY: env-again
env-again: env-clean env

.PHONY: check
check:
	$(PYTHON_EXE) setup.py test

check-install: dist
	$(MAKE) PYTHON_ENV=build/test-$(python)-$(ARCHITECTURE) env-again
	build/test-$(python)-$(ARCHITECTURE)/bin/python$(python) setup.py install
	$(MAKE) PYTHON_ENV=build/test-$(python)-$(ARCHITECTURE) SRCDIR=test check
.PHONY: check-install

build/test-$(python)-$(ARCHITECTURE):
	mkdir -p $(dir $@)
	cp -R $(PYTHON_ENV) $@

dist/$(PROJECT)-$(VERSION).tar.gz: setup.py Makefile check README.txt
	$(PYTHON_EXE) setup.py sdist

README.txt: README.md
	pandoc --from=markdown --to=rst $^ > $@

dist: dist/$(PROJECT)-$(VERSION).tar.gz
.PHONY: dist

published:
	$(PYTHON_ENV)/bin/python setup.py sdist upload

.PHONY: clean
clean:
	rm -rf output/ dist/ build/ MANIFEST README.txt __pycache__/
	find . -name '*.pyc' -o -name '*~' | xargs -r rm -f	

.PHONY: again
again: clean all

