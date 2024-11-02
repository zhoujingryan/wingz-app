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
	@pytest -vv --tb=short -x --ds=wingz.settings.testing wingz* --no-migrations

cov:
	coverage erase
	@pytest -vv --tb=short -x --ds=wingz.settings.testing wingz* --cov-config=./.coveragec --no-migrations --cov-fail-under=95 --cov

cov-html:
	coverage erase
	@pytest -vv --tb=short -x --ds=wingz.settings.testing wingz* --cov-config=./.coveragec --cov-fail-under=95 --cov --cov-report=html
