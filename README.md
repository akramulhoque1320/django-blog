# Django Blog (Dev Notes)

A blog built with **Python and Django 5.2**, using the Django admin for content management.

## Features

- Posts with draft/published status and scheduled publishing
- Categories with post counts in a sidebar
- Search across titles and content
- Pagination (5 posts per page)
- Reader comments with validation and CSRF protection, plus admin approve/hide actions
- Estimated reading time for each post
- Customised Django admin: filters, search, inline comments, editable status
- `seed_blog` command that loads demo content
- 11 automated tests

## Getting started

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_blog          # optional demo posts
python manage.py createsuperuser    # to use the admin
python manage.py runserver
```

- Blog: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Run the tests

```bash
python manage.py test
```

## Production settings

Configure with environment variables:

| Variable | Default |
|----------|---------|
| `DJANGO_SECRET_KEY` | insecure development key |
| `DJANGO_DEBUG` | `1` (set to `0` in production) |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` |

## Project structure

```
config/         # settings and root URLs
blog/
  models.py     # Category, Post (with a published manager), Comment
  views.py      # list (category/search/pagination) and detail with comments
  admin.py      # admin customisation
  forms.py      # comment form
  templates/    # Django templates
  static/       # CSS
  management/commands/seed_blog.py
  tests.py
```
