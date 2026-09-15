from django.contrib import messages
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CommentForm, PostForm, ProfileEditForm, RegisterForm, UserEditForm
from .models import Follow, Like, Post

User = get_user_model()


def register(request):
    if request.user.is_authenticated:
        return redirect("feed")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Conta criada com sucesso.")
        return redirect("feed")
    return render(request, "registration/register.html", {"form": form})


@login_required
def feed(request):
    followed_ids = Follow.objects.filter(follower=request.user).values_list("following_id", flat=True)
    posts = (
        Post.objects.filter(author_id__in=followed_ids)
        .select_related("author", "author__profile")
        .prefetch_related("comments__author", "likes")
        .annotate(like_count=Count("likes", distinct=True))
    )
    return render(
        request,
        "social/feed.html",
        {
            "posts": posts,
            "post_form": PostForm(),
            "comment_form": CommentForm(),
            "following_count": Follow.objects.filter(follower=request.user).count(),
        },
    )


@login_required
def profile_detail(request, username):
    profile_user = get_object_or_404(User.objects.select_related("profile"), username=username)
    posts = (
        profile_user.posts.select_related("author", "author__profile")
        .prefetch_related("comments__author", "likes")
        .annotate(like_count=Count("likes", distinct=True))
    )
    is_following = False
    if request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    context = {
        "profile_user": profile_user,
        "posts": posts,
        "is_following": is_following,
        "followers_count": Follow.objects.filter(following=profile_user).count(),
        "following_count": Follow.objects.filter(follower=profile_user).count(),
        "comment_form": CommentForm(),
    }
    return render(request, "social/profile.html", context)


@login_required
def profile_edit(request):
    profile = request.user.profile
    user_form = UserEditForm(request.POST or None, instance=request.user)
    profile_form = ProfileEditForm(request.POST or None, request.FILES or None, instance=profile)

    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        messages.success(request, "Perfil atualizado com sucesso.")
        return redirect("profile-detail", username=request.user.username)

    return render(
        request,
        "social/profile_edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Senha alterada com sucesso.")
        return redirect("profile-edit")
    return render(request, "social/change_password.html", {"form": form})


@login_required
@require_POST
def toggle_follow(request, username):
    target = get_object_or_404(User, username=username)
    if target == request.user:
        messages.error(request, "Você não pode seguir a si mesmo.")
        return redirect("profile-detail", username=username)

    relation = Follow.objects.filter(follower=request.user, following=target)
    if relation.exists():
        relation.delete()
        messages.info(request, f"Você deixou de seguir @{target.username}.")
    else:
        Follow.objects.create(follower=request.user, following=target)
        messages.success(request, f"Agora você segue @{target.username}.")
    return redirect("profile-detail", username=username)


@login_required
def followers_list(request, username):
    target = get_object_or_404(User, username=username)
    users = User.objects.filter(following_relations__following=target).select_related("profile")
    return render(request, "social/user_list.html", {"users": users, "title": f"Seguidores de @{username}"})


@login_required
def following_list(request, username):
    target = get_object_or_404(User, username=username)
    users = User.objects.filter(follower_relations__follower=target).select_related("profile")
    return render(request, "social/user_list.html", {"users": users, "title": f"@{username} está seguindo"})


@login_required
def user_list(request):
    users = User.objects.exclude(pk=request.user.pk).select_related("profile").order_by("username")
    return render(request, "social/user_list.html", {"users": users, "title": "Descobrir pessoas"})


@login_required
@require_POST
def post_create(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Post publicado.")
    else:
        messages.error(request, "Não foi possível publicar o post.")
    return redirect("feed")


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise Http404

    form = PostForm(request.POST or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Post atualizado.")
        return redirect("profile-detail", username=request.user.username)
    return render(request, "social/post_edit.html", {"form": form, "post": post})


@login_required
@require_POST
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()
    messages.success(request, "Post excluído.")
    return redirect("profile-detail", username=request.user.username)


@login_required
@require_POST
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect(request.POST.get("next") or "feed")


@login_required
@require_POST
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect(request.POST.get("next") or "feed")
