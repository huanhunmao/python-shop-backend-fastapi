.PHONY: install run init test lint

install:
\tpython -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

run:
\tuvicorn app.main:app --reload

init:
\tpython -m app.init_db

test:
\tpytest -q
