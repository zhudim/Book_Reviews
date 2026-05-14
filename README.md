# Book_Reviews
A community-driven platform for discovering, reading, and reviewing books.

## Overview

This Django-based project is a book review platform with user authentication, book listings, review management, reading lists, and admin moderation.

## Requirements

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/Scripts/activate
```

2. Install requirements:

```bash
pip install -r requirements.txt
```

3. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser (optional):

```bash
python manage.py createsuperuser
```

5. Start the development server:

```bash
python manage.py runserver
```

## Notes

- Local development uses SQLite by default.
- To use PostgreSQL, set `USE_SQLITE=false` and configure `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, and `POSTGRES_PORT`.
- The user profile page now shows review and reading list statistics.
