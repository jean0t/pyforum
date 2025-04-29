from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .models import Topic, Reply
from .forms import SignUpForm, TopicForm


def topic_list(request):
    topics = Topic.objects.all().order_by("-created_at")
    return render(request, "forum/topic_list.html", {"topics": topics})


def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    replies = Reply.objects.filter(topic=topic).order_by("-created_at")

    return render(request, "forum/topic_detail.html", {"topic": topic, "replies": replies})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("topic_list")

    else:
        form = SignUpForm()

    return render(request, "forum/signup.html", {"form": form})

@login_required
def custom_logout(request):
    logout(request)
    return redirect("topic_list")

@login_required
def create_topic(request):
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            return redirect("topic_detail", topic_id=topic.id)

    else:
        form = TopicForm()

    return render(request, "forum/create_topic.html", {"form": form})
