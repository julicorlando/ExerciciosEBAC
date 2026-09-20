import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twitterclone.settings")
application = get_wsgi_application()

if os.getenv("VERCEL"):
    try:
        from django.core.management import call_command

        call_command("migrate", interactive=False, verbosity=0)
    except Exception as exc:
        print(f"Aviso: não foi possível executar migrations no cold start: {exc}")
