import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookstore.settings")

application = get_wsgi_application()

if os.getenv("VERCEL") == "1":
    from django.core.management import call_command

    call_command("migrate", interactive=False, verbosity=0)
