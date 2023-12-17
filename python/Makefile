SHELL := /bin/bash
NPROCS = $(shell grep -c 'processor' /proc/cpuinfo)
MAKEFLAGS += -j$(NPROCS)

TARGETS = lsrun
PY_FILES := $(shell find libscape -name \*.py -print)

$(TARGETS):
	shiv . -o lsrun -e libscape.main:main

.PHONY: fmt
fmt:
	isort .
	black .

.PHONY: clean
clean:
	rm -f $(TARGETS)
	rm -rf build/
	rm -rf libscape.egg-info/
	find . -name "__pycache__" -exec rm -rf "{}" +

