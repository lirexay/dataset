.PHONY: run up tests lint migrate create_db db

ALEMBIC_INI=alembic.ini
CREATE_DB_SCRIPT=create_db.py

create_db:
	python3 $(CREATE_DB_SCRIPT)

migrate:
	pdm run alembic -c $(ALEMBIC_INI) upgrade head

db: create_db migrate

run:
	pdm run uvicorn app.main:app --reload

up:
	docker-compose up --build

tests:
	pytest

lint:
	ruff check .
	
init:
	pdm install