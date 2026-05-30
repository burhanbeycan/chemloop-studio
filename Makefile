install:
	pip install -e ".[dev,app]"

test:
	pytest -q

lint:
	ruff check src tests app.py api.py examples

run-api:
	uvicorn api:app --reload

run-app:
	streamlit run app.py

demo:
	chemloop ask "Which electrospinning variables are likely to reduce nanofiber diameter while preserving antimicrobial function?"
