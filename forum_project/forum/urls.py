from django.urls import path
from . import views

urlpatterns = [
    path("", views.topic_list, name="topic_list"),
    path("topic/<int:topic_id>", views.topic_detail, name="topic_detail"),

    path("accounts/signup", views.signup, name="signup"),
    path("logout", views.custom_logout, name="custom_logout"),

    path("create-topic", views.create_topic, name="create_topic"),
]
