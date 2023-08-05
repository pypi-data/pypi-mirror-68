default: build

# Dependencies

bootstrap:
	pip install -e .[dev]

bootstrap-release:
	pip install -e .

.PHONY: bootstrap bootstrap-release

# Build

build:
	python manage.py collectstatic --noinput

release:
	fullrelease

.PHONY: build release

# Packaging

package:
	python setup.py sdist
	python setup.py bdist_wheel

.PHONY: package

# Quality

test:
	python manage.py test

lint: flake8 check-manifest

flake8:
	flake8 --config .flake8

check-manifest:
	check-manifest


.PHONY: lint check-manifest test
