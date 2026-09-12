from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Comment, Follow, Like, Post, Profile
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    PostSerializer,
    ProfileSerializer,
    RegisterSerializer,
    UserPublicSerializer,
)

User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.select_related("profile").order_by("username")
    serializer_class = UserPublicSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related("user").all()
    serializer_class = ProfileSerializer
    http_method_names = ["get", "patch", "put", "head", "options"]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"detail": "Você só pode alterar o próprio perfil."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author", "author__profile").prefetch_related("comments__author", "likes")
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise permissions.PermissionDenied("Você só pode editar seus próprios posts.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise permissions.PermissionDenied("Você só pode excluir seus próprios posts.")
        instance.delete()

    @action(detail=False, methods=["get"])
    def feed(self, request):
        followed_ids = Follow.objects.filter(follower=request.user).values_list("following_id", flat=True)
        posts = self.get_queryset().filter(author_id__in=followed_ids)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            return Response({"liked": False, "likes_count": post.likes.count()})
        return Response({"liked": True, "likes_count": post.likes.count()})

    @action(detail=True, methods=["post"])
    def comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(author=request.user, post=post)
        return Response(CommentSerializer(comment, context={"request": request}).data, status=status.HTTP_201_CREATED)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user).select_related(
            "follower__profile", "following__profile"
        )

    def perform_destroy(self, instance):
        if instance.follower != self.request.user:
            raise permissions.PermissionDenied("Relação não pertence ao usuário autenticado.")
        instance.delete()


class FollowersAPIView(generics.ListAPIView):
    serializer_class = UserPublicSerializer

    def get_queryset(self):
        username = self.kwargs["username"]
        target = get_object_or_404(User, username=username)
        return User.objects.filter(following_relations__following=target).select_related("profile")


class FollowingAPIView(generics.ListAPIView):
    serializer_class = UserPublicSerializer

    def get_queryset(self):
        username = self.kwargs["username"]
        target = get_object_or_404(User, username=username)
        return User.objects.filter(follower_relations__follower=target).select_related("profile")
