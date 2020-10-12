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

badge:
	poetry run coverage-badge -o ./coverage.svg
	poetry run s3cmd -P -s --mime-type=image/svg+xml --host=$$MINIO_HOST --host-bucket=$$MINIO_HOST --access_key=$$MINIO_KEY --secret_key=$$MINIO_SECRET --signature-v2 --no-check-certificate --check-hostname put ./coverage.svg s3://coverage/$${GITHUB_REPOSITORY}/coverage.svg

release:
	git checkout develop
	git pull
	make test
	make check-fixtures
	make check-code-style
	poetry version patch
	git add pyproject.toml
	git commit -m "Bump version"
	git flow release start -F "v$$(poetry version --short)"
	git flow release finish -m "v$$(poetry version --short)" -F -D -p

publish:
	poetry publish --build --username=__token__ --password=$$PYPI_TOKEN
