from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from .models import Comment, User
from .forms import CommentForm


def add_comment(request) -> HttpResponseRedirect | HttpResponse:
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            # Check if the user already exists with the provided email
            user = User.objects.filter(
                email=form.cleaned_data["email"]
            ).first()

            # If user doesn't exist, create a new user
            if not user:
                user = User(
                    username=form.cleaned_data["username"],
                    email=form.cleaned_data["email"],
                    home_page=form.cleaned_data.get("homepage", ""),
                )
                user.save()

            parent_comment_id = request.POST.get("parent_comment_id")
            if parent_comment_id:
                parent_comment = get_object_or_404(
                    Comment, pk=parent_comment_id
                )
                reply = Comment(
                    user=user,
                    text=form.cleaned_data["text"],
                    parent_comment=parent_comment,
                )
                reply.save()
            else:
                # If not a reply, it's a top-level comment
                comment = Comment(
                    user=user,
                    text=form.cleaned_data["text"],
                )
                comment.save()

            # Redirect to the comment list page or any other desired page
            return redirect("comments:comment_list")
    else:
        form = CommentForm()

    return render(request, "comments/add_comment.html", {"form": form})


def comment_list(request) -> HttpResponse:
    sort_by = request.GET.get("sort_by", "-created_at")
    comments = Comment.objects.filter(parent_comment=None).order_by(sort_by)
    paginator = Paginator(comments, 25)
    page = request.GET.get("page")
    comments = paginator.get_page(page)
    return render(
        request, "comments/comment_list.html", {"comments": comments}
    )


def comment_detail(request, comment_id) -> HttpResponseRedirect | HttpResponse:
    comment = get_object_or_404(Comment, pk=comment_id)
    replies = comment.replies.all()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            user, created = User.objects.get_or_create(
                email=form.cleaned_data["email"],
                defaults={"username": form.cleaned_data["username"]},
            )

            reply = Comment(
                user=user,
                text=form.cleaned_data["text"],
                parent_comment=comment,
            )
            reply.save()

            return HttpResponseRedirect(
                request.path
            )  # Redirect to the same page after adding a comment
    else:
        form = CommentForm()

    return render(
        request,
        "comments/comment_detail.html",
        {"comment": comment, "replies": replies, "form": form},
    )
