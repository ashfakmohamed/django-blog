from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import BlogPostForm, UserRegisterForm
from .models import BlogPost


def home(request):
    posts = BlogPost.objects.select_related("author")
    page = Paginator(posts, 10).get_page(request.GET.get("page"))
    return render(request, "blog/home.html", {"page": page})


def post_detail(request, post_id):
    post = get_object_or_404(BlogPost.objects.select_related("author"), pk=post_id)
    return render(request, "blog/post_detail.html", {"post": post})


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = UserRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account is ready.")
        return redirect("home")
    return render(request, "registration/register.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def create_post(request):
    form = BlogPostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Post published.")
        return redirect("post_detail", post_id=post.pk)
    return render(request, "blog/post_form.html", {"form": form, "heading": "Create post"})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id, author=request.user)
    form = BlogPostForm(request.POST or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Post updated.")
        return redirect("post_detail", post_id=post.pk)
    return render(request, "blog/post_form.html", {"form": form, "heading": "Edit post"})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id, author=request.user)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect("home")
    return render(request, "blog/post_confirm_delete.html", {"post": post})
