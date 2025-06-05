install:
	uv pip install -r requirements.txt

create_admin:
	uv run python manage.py createsuperuser

create_app_layer:
	@read -p "Input AppLayer name: " name; \
	.venv/bin/python manage.py startapp "$$name" && mv "$$name" task_manager/


make_migrate:
	uv run python manage.py makemigrations

migrate:
	uv run python manage.py migrate

test:
	uv run python3 manage.py test

test-coverage:
	uv run coverage run manage.py test
	uv run coverage report -m --include=task_manager/* --omit=task_manager/settings.py
	uv run coverage xml --include=task_manager/* --omit=task_manager/settings.py

collectstatic:
	uv run python manage.py collectstatic --noinput

run:
	uv run python manage.py runserver

generate-ru-local:
	uv run django-admin makemessages -l ru

render-start:
	gunicorn task_manager.wsgi

build:
	./build.sh

lint_pre-commit:
	uv run pre-commit run --all-files

fix:
	uv run ruff check --fix
