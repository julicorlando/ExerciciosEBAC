import hashlib
import hmac
import json
import os
from pathlib import Path

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from git import GitCommandError, Repo
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok", "project": "bookstore"})


def hello(request):
    commit = "indisponível"

    try:
        repo = Repo(settings.BASE_DIR, search_parent_directories=True)
        commit = repo.head.commit.hexsha[:7]
    except Exception:
        pass

    return render(
        request,
        "hello_world.html",
        {
            "status": "Bookstore online",
            "commit": commit,
        },
    )


def _valid_github_signature(request):
    secret = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    if not secret:
        return True

    signature = request.headers.get("X-Hub-Signature-256", "")
    if not signature.startswith("sha256="):
        return False

    expected = hmac.new(
        secret.encode("utf-8"),
        request.body,
        hashlib.sha256,
    ).hexdigest()

    received = signature.removeprefix("sha256=")
    return hmac.compare_digest(expected, received)


@csrf_exempt
@require_POST
def update_server(request):
    if not _valid_github_signature(request):
        return JsonResponse(
            {"status": "error", "detail": "assinatura inválida"},
            status=403,
        )

    if request.headers.get("X-GitHub-Event") != "push":
        return JsonResponse({"status": "ignored", "detail": "evento ignorado"})

    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse(
            {"status": "error", "detail": "payload inválido"},
            status=400,
        )

    expected_repository = os.getenv(
        "GITHUB_REPOSITORY",
        "julicorlando/ExerciciosEBAC",
    )
    repository = payload.get("repository", {}).get("full_name")

    if repository != expected_repository:
        return JsonResponse(
            {"status": "error", "detail": "repositório não autorizado"},
            status=403,
        )

    deploy_branch = os.getenv("DEPLOY_BRANCH", "main")
    if payload.get("ref") != f"refs/heads/{deploy_branch}":
        return JsonResponse(
            {
                "status": "ignored",
                "detail": f"somente a branch {deploy_branch} realiza deploy",
            }
        )

    try:
        repo = Repo(settings.BASE_DIR, search_parent_directories=True)

        if not repo.head.is_detached and repo.active_branch.name != deploy_branch:
            repo.git.checkout(deploy_branch)

        origin = repo.remotes.origin
        origin.pull(deploy_branch)

        wsgi_file = os.getenv("PYTHONANYWHERE_WSGI_FILE", "")
        if wsgi_file:
            path = Path(wsgi_file)
            if path.exists():
                path.touch()

        commit = repo.head.commit.hexsha[:7]
    except (GitCommandError, OSError, ValueError) as exc:
        return JsonResponse(
            {"status": "error", "detail": str(exc)},
            status=500,
        )

    return render(
        request,
        "hello_world.html",
        {
            "status": "Deploy atualizado com sucesso",
            "commit": commit,
        },
    )
