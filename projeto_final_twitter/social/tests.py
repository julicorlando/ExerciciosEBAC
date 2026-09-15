from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Comment, Follow, Like, Post

User = get_user_model()


class SocialWebTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="julio", password="SenhaForte123!", email="julio@example.com")
        self.followed = User.objects.create_user(username="ana", password="SenhaForte123!")
        self.stranger = User.objects.create_user(username="bruno", password="SenhaForte123!")
        self.client.login(username="julio", password="SenhaForte123!")

    def test_profile_is_created_with_user(self):
        self.assertEqual(self.user.profile.user, self.user)

    def test_feed_contains_only_posts_from_followed_users(self):
        Follow.objects.create(follower=self.user, following=self.followed)
        Post.objects.create(author=self.followed, content="post da pessoa seguida")
        Post.objects.create(author=self.stranger, content="post de pessoa não seguida")
        Post.objects.create(author=self.user, content="meu próprio post")

        response = self.client.get(reverse("feed"))

        self.assertContains(response, "post da pessoa seguida")
        self.assertNotContains(response, "post de pessoa não seguida")
        self.assertNotContains(response, "meu próprio post")

    def test_follow_and_unfollow_user(self):
        url = reverse("toggle-follow", kwargs={"username": self.followed.username})
        self.client.post(url)
        self.assertTrue(Follow.objects.filter(follower=self.user, following=self.followed).exists())

        self.client.post(url)
        self.assertFalse(Follow.objects.filter(follower=self.user, following=self.followed).exists())

    def test_user_cannot_follow_self(self):
        url = reverse("toggle-follow", kwargs={"username": self.user.username})
        self.client.post(url)
        self.assertFalse(Follow.objects.filter(follower=self.user, following=self.user).exists())

    def test_create_edit_and_delete_own_post(self):
        self.client.post(reverse("post-create"), {"content": "primeiro texto"})
        post = Post.objects.get(author=self.user)

        self.client.post(reverse("post-edit", kwargs={"pk": post.pk}), {"content": "texto editado"})
        post.refresh_from_db()
        self.assertEqual(post.content, "texto editado")

        self.client.post(reverse("post-delete", kwargs={"pk": post.pk}))
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())

    def test_like_is_toggleable_and_unique(self):
        post = Post.objects.create(author=self.followed, content="curta aqui")
        url = reverse("toggle-like", kwargs={"pk": post.pk})

        self.client.post(url)
        self.assertEqual(Like.objects.filter(user=self.user, post=post).count(), 1)

        self.client.post(url)
        self.assertEqual(Like.objects.filter(user=self.user, post=post).count(), 0)

    def test_authenticated_user_can_comment(self):
        post = Post.objects.create(author=self.followed, content="comente aqui")
        self.client.post(reverse("add-comment", kwargs={"pk": post.pk}), {"content": "meu comentário"})
        self.assertTrue(Comment.objects.filter(author=self.user, post=post, content="meu comentário").exists())

    def test_profile_fields_are_optional_and_can_be_changed(self):
        response = self.client.post(
            reverse("profile-edit"),
            {"first_name": "Júlio", "last_name": "Orlando", "email": "novo@example.com", "bio": "Backend Python"},
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.first_name, "Júlio")
        self.assertEqual(self.user.profile.bio, "Backend Python")

    def test_password_can_be_changed(self):
        response = self.client.post(
            reverse("change-password"),
            {
                "old_password": "SenhaForte123!",
                "new_password1": "NovaSenhaForte456!",
                "new_password2": "NovaSenhaForte456!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(authenticate(username="julio", password="NovaSenhaForte456!"))

    def test_registration_page_loads_for_anonymous_user(self):
        self.client.logout()
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Criar sua conta")

    def test_registration_web_creates_and_authenticates_user(self):
        self.client.logout()
        response = self.client.post(
            reverse("register"),
            {
                "username": "novo_web",
                "first_name": "Novo",
                "last_name": "Usuário",
                "email": "novo-web@example.com",
                "password1": "SenhaNovaForte789!",
                "password2": "SenhaNovaForte789!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="novo_web").exists())
        self.assertEqual(int(self.client.session["_auth_user_id"]), User.objects.get(username="novo_web").pk)


class SocialAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apiuser", password="SenhaForte123!", email="api@example.com")
        self.followed = User.objects.create_user(username="seguido", password="SenhaForte123!")
        self.other = User.objects.create_user(username="outro", password="SenhaForte123!")
        self.token = Token.objects.create(user=self.user)
        self.api = APIClient()
        self.api.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_api_registration_creates_user_securely(self):
        anonymous = APIClient()
        response = anonymous.post(
            reverse("api-register"),
            {
                "username": "novo",
                "email": "novo@example.com",
                "password": "SenhaNovaForte789!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.get(username="novo").check_password("SenhaNovaForte789!"))

    def test_api_feed_returns_only_followed_posts(self):
        Follow.objects.create(follower=self.user, following=self.followed)
        included = Post.objects.create(author=self.followed, content="aparece")
        Post.objects.create(author=self.other, content="não aparece")

        response = self.api.get(reverse("api-posts-feed"))

        self.assertEqual(response.status_code, 200)
        ids = {item["id"] for item in response.json()}
        self.assertEqual(ids, {included.id})

    def test_api_post_crud_and_owner_protection(self):
        response = self.api.post(reverse("api-posts-list"), {"content": "via API"}, format="json")
        self.assertEqual(response.status_code, 201)
        post_id = response.json()["id"]

        response = self.api.patch(reverse("api-posts-detail", kwargs={"pk": post_id}), {"content": "editado"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.get(pk=post_id).content, "editado")

        foreign_post = Post.objects.create(author=self.other, content="de outro")
        response = self.api.patch(reverse("api-posts-detail", kwargs={"pk": foreign_post.pk}), {"content": "tentativa"}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_api_like_and_comment(self):
        post = Post.objects.create(author=self.followed, content="interagir")
        like_url = reverse("api-posts-like", kwargs={"pk": post.pk})
        comment_url = reverse("api-posts-comment", kwargs={"pk": post.pk})

        self.assertTrue(self.api.post(like_url).json()["liked"])
        self.assertFalse(self.api.post(like_url).json()["liked"])

        response = self.api.post(comment_url, {"content": "comentário REST"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Comment.objects.filter(post=post, author=self.user).exists())

    def test_api_follow_rejects_self_follow(self):
        response = self.api.post(reverse("api-follows-list"), {"following_id": self.user.pk}, format="json")
        self.assertEqual(response.status_code, 400)
