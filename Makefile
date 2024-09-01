generate:
	rm -rf dist && pipenv run python -m build
release:
	pipenv run python -m twine upload dist/*
