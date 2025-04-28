from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    title = models.CharField(max_length=128)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Reply(models.Model):
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author.username} on {self.topic.title}"
