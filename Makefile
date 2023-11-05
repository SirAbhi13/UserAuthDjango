runserver:
	python3 src/manage.py runserver

setup:
	python3 -m pip install poetry
	poetry install
	cp .env.example .env
