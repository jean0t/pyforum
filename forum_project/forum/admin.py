from django.contrib import admin
from .models import Topic, Reply

# Register your models here.
class TopicAdmin(admin.ModelAdmin):
    fields = ["title", "body", "author"]
    list_display = ("title", "author", "created_at")

class ReplyAdmin(admin.ModelAdmin):
    fields = ["body", "author", "topic"]
    list_display = ("author", "topic", "created_at")

admin.site.register(Topic, TopicAdmin)
admin.site.register(Reply, ReplyAdmin)
