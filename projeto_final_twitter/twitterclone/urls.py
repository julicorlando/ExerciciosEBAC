import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from django.urls import include, path, re_path
from django.views.static import serve
from rest_framework.authtoken.views import obtain_auth_token

from social import views as social_views


def health(request):
    return JsonResponse({"status": "ok", "project": "twitter-clone"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", social_views.feed, name="feed"),
    path("health/", health, name="health"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("cadastro/", social_views.register, name="register"),
    path("perfil/editar/", social_views.profile_edit, name="profile-edit"),
    path("perfil/<str:username>/", social_views.profile_detail, name="profile-detail"),
    path("perfil/<str:username>/seguir/", social_views.toggle_follow, name="toggle-follow"),
    path("perfil/<str:username>/seguidores/", social_views.followers_list, name="followers-list"),
    path("perfil/<str:username>/seguindo/", social_views.following_list, name="following-list"),
    path("usuarios/", social_views.user_list, name="user-list"),
    path("posts/criar/", social_views.post_create, name="post-create"),
    path("posts/<int:pk>/editar/", social_views.post_edit, name="post-edit"),
    path("posts/<int:pk>/excluir/", social_views.post_delete, name="post-delete"),
    path("posts/<int:pk>/curtir/", social_views.toggle_like, name="toggle-like"),
    path("posts/<int:pk>/comentar/", social_views.add_comment, name="add-comment"),
    path("senha/", social_views.change_password, name="change-password"),
    path("api/token/", obtain_auth_token, name="api-token"),
    path("api/", include("social.api_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif os.getenv("VERCEL"):
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
