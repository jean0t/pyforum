from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic
from .forms import SignUpForm
from django.contrib.auth import login


def topic_list(request):
    topics = Topic.objects.all().order_by("-created_at")
    return render(request, "forum/topic_list.html", {"topics": topics})


def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    replies = Reply.objects.filter(topic=topic).order_by("-created_at")

    return render(request, "forum/topic_detail.html", {"topic": topic, "replies": replies})


def signup(request):
    if request.method == "POST":
        form = SingUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("topic_list")

    else:
        form = SignUpForm()

    return render(request, "forum/signup.html", {"form": form})
