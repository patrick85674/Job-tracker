dev-start:
	python manage.py runserver --settings=config.settings.dev

dev-install:
	pip install -r requirements/dev.txt

dev-showmigrations:
	python manage.py showmigrations --settings=config.settings.dev

dev-makemigrations:
	python manage.py makemigrations --settings=config.settings.dev

dev-migrate:
	python manage.py migrate --settings=config.settings.dev

dev-test:
	python manage.py test $(route) --settings=config.settings.dev

create-secret:
	python -c "import secrets; print(secrets.token_urlsafe(50))"

