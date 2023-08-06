release:
	python3 setup.py sdist --formats=gztar

documentation: doc/build doc/help.txt doc/pydoc/stepic.html stepic.1

doc/build:
	virtualenv --python=python3 --system-site-packages venv1
	python3 setup.py bdist_wheel
	./venv1/bin/pip install -f dist/ stepic

doc/help.txt: doc/build
	./venv1/bin/stepic --help > doc/help.txt

doc/pydoc/stepic.html: doc/build
	./venv1/bin/python -m pydoc -w stepic
	mkdir -p doc/pydoc/
	mv stepic.html doc/pydoc/

stepic.1: stepic.help2man_include doc/build
	help2man --include=stepic.help2man_include --output=stepic.1 ./venv1/bin/stepic

clean:
	python3 setup.py clean
	-rm -rf build MANIFEST
	-find -name "*.py[co]" -print0 | xargs -0 rm
	-rm -rf venv1

.PHONY: doc/build release documentation clean
