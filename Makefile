clean:
	find . -name '*.py[cod]' -delete
	find . -name '__pycache__' -delete
	find . -name '*.c' -delete
	find . -name '*.h' -delete
	find . -name '*.so' -delete
	find . -name '*.html' -delete

lines:
	find . -name "*.py" | xargs cat | wc -l

check:
	pre-commit run --all-files

style:
	@flake8 .

test:
	@pytest -vv --tb=short -x --ds=wingz.settings.testing --no-migrations

test-cov:
	coverage erase
	@pytest -vv --tb=short -x --ds=wingz.settings.testing --cov-config=./.coveragec --no-migrations --cov-fail-under=95 --cov
