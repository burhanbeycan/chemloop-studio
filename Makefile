# ChemLoop Studio convenience commands

.PHONY: install run-app run-api test

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

run-app:
	streamlit run app/Home.py

run-api:
	uvicorn mds.api:app --reload --port 8000

test:
	pytest -q
