main: fix-isort fix-yapf check-code-style test check-fixtures

test:
	poetry run py.test --ff --cov dypendence

test-report:
	poetry run py.test --ff --cov dypendence --html=report.html --self-contained-html

check-fixtures:
	poetry run py.test dypendence --dead-fixtures --dup-fixtures

check-yapf:
	poetry run yapf -d -r -p dypendence

fix-yapf:
	poetry run yapf -i -r -p dypendence

check-isort:
	poetry run isort -c dypendence

fix-isort:
	poetry run isort dypendence

reformat-files: fix-yapf fix-isort

check-code-style: check-isort check-yapf
	poetry run flake8 dypendence

make-badge:
	poetry run coverage-badge -o ./coverage.svg

release:
	git checkout develop
	make test
	make check-fixtures
	make check-code-style
	poetry version patch
	git add pyproject.toml
	git commit -m "Bump version"
	git flow release start -F "$$(poetry version --short)"
	git flow release finish -m "$$(poetry version --short)" -F -D -p

publish:
	poetry publish --build
