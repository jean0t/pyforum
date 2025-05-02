from django.urls import path
from . import views

urlpatterns = [
    path("", views.topic_list, name="topic_list"),

    path("topic/<int:topic_id>", views.topic_detail, name="topic_detail"),
    path("topic/<int:topic_id>/edit", views.edit_topic, name="edit_topic"),
    path("topic/<int:topic_id>/delete", views.delete_topic, name="delete_topic"),

    path("topic/<int:topic_id>/reply/<int:reply_id>/edit", views.edit_reply, name="edit_reply"),
    path("topic/<int:topic_id>/reply/<int:reply_id>/delete", views.delete_reply, name="delete_reply"),

    path("accounts/signup", views.signup, name="signup"),
    path("logout", views.custom_logout, name="custom_logout"),

    path("create-topic", views.create_topic, name="create_topic"),
]
