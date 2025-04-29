from django.urls import path
from . import views

urlpatterns = [
    path("", views.topic_list, name="topic_list"),
    path("topic/<int:topic_id>", views.topic_detail, name="topic_detail"),
    path("signup", views.signup, name="signup"),
]
