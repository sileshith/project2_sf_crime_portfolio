.PHONY: install build evaluate test lint check app

install:
	uv sync --extra dev

build:
	uv run sf-incidents-build --source cleanedData/sfpd_clean_2018_2025.csv

evaluate:
	uv run sf-incidents-evaluate

test:
	uv run pytest

lint:
	uv run ruff check .

check: lint test

app:
	uv run streamlit run app.py

