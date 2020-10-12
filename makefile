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

check-code-style: check-isort check-yapf
	poetry run flake8 dypendence

make-badge:
	poetry run coverage-badge -o ./coverage.svg

reformat-files: fix-yapf fix-isort

all: fix-isort fix-yapf check-code-style test check-fixtures
