#
# Recipes for running Jupyter examples in a Python virtenv 
# and trying out package in a venv.
#
.PHONY: run_examples

run_examples: clean_virtualenv activate_virtualenv
	.venv/bin/pip install jupyterlab
	.venv/bin/python setup.py install
	.venv/bin/jupyter notebook example/time_motif.ipynb
	
clean_virtualenv:
	-rm -r .venv/

activate_virtualenv: clean_virtualenv
	python3 -m venv .venv

clean_build:
	-rm -r build/*
	-rm -r dist/*

	
