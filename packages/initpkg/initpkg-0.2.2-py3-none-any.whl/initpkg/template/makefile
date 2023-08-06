.PHONY: docs
setup:
	rm -rf build
	rm -rf dist
	python setup.py bdist_wheel
dev:
	python setup.py develop
install:
	pip uninstall  $(name) -y
	pip install --find-links=dist  --no-cache-dir $(name)
test:
	pytest tests -vvv
docs:
	rm -rf docs/_build && sphinx-apidoc -o docs $(name) && cd docs && make html