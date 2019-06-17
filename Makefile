SHELL=/bin/bash
CONDA_PATH = ~/anaconda3
ENVIROMENT_NAME_CREATE = api_deposit_fiat
ENVIROMENT_NAME_REMOVE = warning
VAR_FLASK_APP=run.py

install:
	pip install -r requirements.txt
	pip freeze > requirements.txt

run:
	export FLASK_APP=$(VAR_FLASK_APP) && flask run

ron:
	python manage.py runserver

babel-make:
	pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
	pybabel init -i messages.pot -d translations -l es
	pybabel init -i messages.pot -d translations -l de
	pybabel init -i messages.pot -d translations -l it
	pybabel init -i messages.pot -d translations -l pt
	pybabel init -i messages.pot -d translations -l en

babel-build:
	pybabel compile -d translations

babel-update:
	pybabel update -i messages.pot -d translations

revert:
	git checkout .

marko:
	( \
	   yes y | conda create -n $(ENVIROMENT_NAME_CREATE) python=3.6; \
	   source $(CONDA_PATH)/bin/activate $(ENVIROMENT_NAME_CREATE); \
	   yes y | pip install -r requirements.txt; \
	   echo "saliendo....."; \
	   source deactivate; \
	)

remove:
	yes | conda remove --name $(ENVIROMENT_NAME_REMOVE) --all

pucho:
	git add .
	git commit -m $(m)
	git push origin feature/estructura

pol:
	git add .
	git commit -m $(m)
	git pull origin feature/estructura

cometa:
	git add .
	git commit -m $(m)
