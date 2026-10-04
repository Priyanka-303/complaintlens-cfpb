.PHONY: setup download build validate figures test all

setup:
	python -m pip install -r requirements.txt

download:
	python src/download_data.py

build:
	python src/build_marts.py

validate:
	python src/validate_data.py

figures:
	python src/create_figures.py

test:
	python -m unittest discover -s tests -v

all: build validate figures test
