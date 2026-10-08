# Django Blog

<!-- profile-upgrade -->
[![Django CI](https://github.com/ashfakmohamed/django-blog/actions/workflows/ci.yml/badge.svg)](https://github.com/ashfakmohamed/django-blog/actions/workflows/ci.yml)

**Stack:** Python · Django · HTML · CSS

A small Django publishing app with public reading and authenticated writing.

## Security and behavior

- Anyone can read posts.
- Registration uses Django password hashing and validation.
- Only a post's author can edit or delete it.
- Post ownership is assigned server-side, never accepted from form data.
- Logout is a CSRF-protected POST action.
- Secrets, debug mode, and allowed hosts come from environment variables.
- Local databases and virtual environments are excluded from Git.

## Local setup

~~~powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
~~~

Set the variables shown in `.env.example` in your shell or deployment platform. Production must use a strong `DJANGO_SECRET_KEY`, correct `DJANGO_ALLOWED_HOSTS`, and `DJANGO_DEBUG=False`.

## Checks

~~~powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
~~~

## Engineering quality

- GitHub Actions runs Django checks and the automated test suite on every push.
- Runtime configuration is documented through `.env.example`; secrets are not committed.
- Local databases, uploaded media, caches, and virtual environments are excluded from version control.
- Security-sensitive behavior and authorization rules are documented above.