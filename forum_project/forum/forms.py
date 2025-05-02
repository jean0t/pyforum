from django import forms
from .models import Topic, Reply

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class TopicForm(forms.ModelForm):
    """
    Form to create and edit Forum Topics
    """
    class Meta:
        model = Topic
        fields = ["title", "body"]

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Topic Title"}),
            "body": forms.Textarea(attrs={"rows": 5, "placeholder": "Write your topic here..."}),
        }


class ReplyForm(forms.ModelForm):
    """
    Form responsible to the replies to a Topic.
    """
    class Meta:
        model = Reply
        fields = ["body"]
        labels = {"body": "Your reply"}

        widgets = {
            "body": forms.Textarea(attrs={"rows": 4, "cols": 40, "placeholder": "Write your reply..."}),
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password do not match.")

        return cleaned_data
