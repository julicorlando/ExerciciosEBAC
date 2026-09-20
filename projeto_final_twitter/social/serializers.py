from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Comment, Follow, Like, Post, Profile

User = get_user_model()


class UserPublicSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "avatar")

    def get_avatar(self, obj):
        profile = getattr(obj, "profile", None)
        if profile and profile.avatar:
            request = self.context.get("request")
            url = profile.avatar.url
            return request.build_absolute_uri(url) if request else url
        return None


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "password")
        extra_kwargs = {"email": {"required": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "user", "bio", "avatar")


class CommentSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "author", "content", "created_at")
        read_only_fields = ("id", "author", "created_at")


class PostSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    liked_by_me = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "content",
            "created_at",
            "updated_at",
            "likes_count",
            "liked_by_me",
            "comments",
        )
        read_only_fields = ("id", "author", "created_at", "updated_at")

    def get_liked_by_me(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return Like.objects.filter(user=request.user, post=obj).exists()


class FollowSerializer(serializers.ModelSerializer):
    follower = UserPublicSerializer(read_only=True)
    following = UserPublicSerializer(read_only=True)
    following_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="following",
        write_only=True,
    )

    class Meta:
        model = Follow
        fields = ("id", "follower", "following", "following_id", "created_at")
        read_only_fields = ("id", "follower", "following", "created_at")

    def validate_following_id(self, value):
        request = self.context["request"]
        if value == request.user:
            raise serializers.ValidationError("Você não pode seguir a si mesmo.")
        return value

    def create(self, validated_data):
        follower = self.context["request"].user
        following = validated_data["following"]
        relation, created = Follow.objects.get_or_create(follower=follower, following=following)
        if not created:
            raise serializers.ValidationError("Você já segue este usuário.")
        return relation
