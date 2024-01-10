# To create a virtual env.
create-venv:
	python -m pipenv install

# To shell into the virtual env.
shell-env:
	python -m pipenv shell

# To install a package into the venv
install-package:
	python -m pipenv install selenium

# To run an ung web scraping script
run_ung:
	python ./ung.py

