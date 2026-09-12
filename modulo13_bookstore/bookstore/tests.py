import json
import os
from unittest.mock import MagicMock, patch

from django.test import TestCase
from django.urls import reverse


class HealthEndpointTest(TestCase):
    def test_health_endpoint_uses_drf(self):
        response = self.client.get(reverse("health"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"status": "ok", "project": "bookstore"},
        )


class ContinuousDeliveryViewsTest(TestCase):
    @patch("bookstore.views.Repo")
    def test_hello_page_displays_current_commit(self, repo_class):
        repo = MagicMock()
        repo.head.commit.hexsha = "abc1234def5678"
        repo_class.return_value = repo

        response = self.client.get(reverse("hello"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bookstore online")
        self.assertContains(response, "abc1234")

    @patch("bookstore.views.Repo")
    def test_github_push_updates_server(self, repo_class):
        repo = MagicMock()
        repo.head.is_detached = False
        repo.active_branch.name = "main"
        repo.head.commit.hexsha = "fedcba987654321"
        repo_class.return_value = repo

        payload = {
            "ref": "refs/heads/main",
            "repository": {"full_name": "julicorlando/ExerciciosEBAC"},
        }

        with patch.dict(
            os.environ,
            {
                "GITHUB_REPOSITORY": "julicorlando/ExerciciosEBAC",
                "DEPLOY_BRANCH": "main",
            },
            clear=False,
        ):
            response = self.client.post(
                reverse("update-server"),
                data=json.dumps(payload),
                content_type="application/json",
                HTTP_X_GITHUB_EVENT="push",
            )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Deploy atualizado com sucesso")
        repo.remotes.origin.pull.assert_called_once_with("main")

    def test_webhook_rejects_another_repository(self):
        payload = {
            "ref": "refs/heads/main",
            "repository": {"full_name": "outro/projeto"},
        }

        with patch.dict(
            os.environ,
            {
                "GITHUB_REPOSITORY": "julicorlando/ExerciciosEBAC",
                "DEPLOY_BRANCH": "main",
            },
            clear=False,
        ):
            response = self.client.post(
                reverse("update-server"),
                data=json.dumps(payload),
                content_type="application/json",
                HTTP_X_GITHUB_EVENT="push",
            )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["status"], "error")
