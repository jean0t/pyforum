# application layer
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

# authentication
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

# app specific
from .models import Topic, Reply
from .forms import SignUpForm, TopicForm, ReplyForm
from .cache import get_topics, get_replies, update_replies_cache


def topic_list(request):
    topics = get_topics(request)
    return render(request, "forum/topic_list.html", {"topics": topics})


def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    replies = get_replies(topic, topic_id)

    if request.method == "POST":
        if request.user.is_authenticated:
            form = ReplyForm(request.POST)
            if form.is_valid():
                reply = form.save(commit=False)
                reply.topic = topic
                reply.author = request.user
                reply.save()
                update_replies_cache(topic_id, topic)
                return redirect("topic_detail", topic_id=topic.id)
        else:
            return redirect("login")

    else:
        form = ReplyForm()

    return render(request, "forum/topic_detail.html", {"topic": topic, "replies": replies, "form": form})


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


@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if topic.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this topic.")

    if request.method == "POST":
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            update_topics_cache()
            return redirect("topic_detail", topic_id=topic.id)

    else:
        form = TopicForm(instance=topic)

    return render(request, "forum/edit_topic.html", {"form": form})


@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if topic.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this topic.")

    if request.method == "POST":
        topic.delete()
        update_topics_cache(topic_id, topic)
        return redirect("topic_list")

    return render(request, "forum/delete_topic.html", {"topic": topic})

@login_required
def edit_reply(request, topic_id, reply_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    reply = get_object_or_404(Reply, pk=reply_id)
    if reply.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this reply.")

    if request.method == "POST":
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            form.save()
            update_replies_cache(topic_id, topic)
            return redirect("topic_detail", topic_id=topic_id)

    else:
        form = ReplyForm(instance=reply)

    return render(request, "forum/edit_reply.html", {"form": form})

@login_required
def delete_reply(request, topic_id, reply_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    reply = get_object_or_404(Reply, pk=reply_id)
    if reply.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this reply.")

    if request.method == "POST":
        reply.delete()
        update_replies_cache(topic_id, topic)
        return redirect("topic_detail", topic_id=topic_id)

    return render(request, "forum/delete_reply.html", {"reply": reply})
