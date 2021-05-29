.PHONY: all tests dependencies unit functional tdd-functional tdd-unit run clean black

PACKAGE_PATH		:= ./fragdenstaat_client
MAIN_CLI_NAME		:= fragdenstaat-client
GIT_ROOT			:= $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
VENV_ROOT			:= $(GIT_ROOT)/.venv
MAIN_CLI_PATH		:= $(VENV_ROOT)/$(MAIN_CLI_NAME)
export VENV			?= $(VENV_ROOT)
all: dependencies tests

venv $(VENV):  # creates $(VENV) folder if does not exist
	python3 -mvenv $(VENV)
	$(VENV)/bin/pip install -U pip setuptools

develop $(MAIN_CLI_PATH) $(VENV)/bin/pytest $(VENV)/bin/python $(VENV)/bin/pip: # installs latest pip
	test -e $(VENV)/bin/pip || $(MAKE) $(VENV)
	$(VENV)/bin/pip install -r development.txt
	$(VENV)/bin/python setup.py develop

# Runs the unit and functional tests
tests: unit functional  # runs all tests


# Install dependencies
dependencies: | $(VENV)/bin/pytest
	$(VENV)/bin/pip install -r development.txt
	$(VENV)/bin/python setup.py develop


# runs unit tests
unit: | $(VENV)/bin/pytest  # runs only unit tests
	$(VENV)/bin/pytest  --capture=no


# runs functional tests
functional:| $(VENV)/bin/pytest  # runs functional tests
	$(VENV)/bin/pytest --capture=no tests/functional

run: | $(VENV)/bin/python
	@$(MAIN_CLI_PATH) --help

push-release:  # pushes distribution tarballs of the current version
	$(VENV)/bin/twine check dist/*.tar.gz
	$(VENV)/bin/twine upload dist/*.tar.gz

build-release:
	rm -rf ./dist  # remove local packages
	$(VENV)/bin/twine check dist/*.tar.gz
	$(VENV)/bin/twine upload dist/*.tar.gz

release: tests build-release push-release
	$(MAKE) build-release
	$(MAKE) push-release

clean:
	rm -rf .venv

black:
	black -l 79 $(PACKAGE_PATH) tests
