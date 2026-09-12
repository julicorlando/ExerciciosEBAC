from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import (
    FollowViewSet,
    FollowersAPIView,
    FollowingAPIView,
    PostViewSet,
    ProfileViewSet,
    RegisterAPIView,
    UserViewSet,
)

router = DefaultRouter()
router.register("users", UserViewSet, basename="api-users")
router.register("profiles", ProfileViewSet, basename="api-profiles")
router.register("posts", PostViewSet, basename="api-posts")
router.register("follows", FollowViewSet, basename="api-follows")

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="api-register"),
    path("users/<str:username>/followers/", FollowersAPIView.as_view(), name="api-followers"),
    path("users/<str:username>/following/", FollowingAPIView.as_view(), name="api-following"),
    path("", include(router.urls)),
]
