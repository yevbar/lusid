generate:
	pipenv run python -m build
release:
	pipenv run python -m twine upload dist/*
