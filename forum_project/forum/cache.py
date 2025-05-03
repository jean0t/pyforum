from django.core.cache import cache
from .models import Topic

CACHE_TIME = 60*3 # 3 minutes
TOPICS_CACHE_KEY = "topics_cache"

def get_replies_cache_key(topic_id):
    return f"topic_{topic_id}_replies"


def get_topics(request):
    cache_key = TOPICS_CACHE_KEY
    topics = cache.get(cache_key)
    if topics is None:
        topics = Topic.objects.all().order_by("-created_at")
        cache.set(cache_key, topics, timeout=CACHE_TIME)

    return topics


def get_replies(topic, topic_id):
    cache_key = get_replies_cache_key(topic_id)
    replies = cache.get(cache_key)
    if replies is None:
        replies = topic.reply_set.order_by("-created_at")
        cache.set(cache_key, replies, timeout=CACHE_TIME)

    return replies


def update_topics_cache():
    cache_key = TOPICS_CACHE_KEY
    topic = Topic.objects.all().order_by("-created_at")
    cache.set(cache_key, topics, timeout=CACHE_TIME)


def update_replies_cache(topic_id, topic):
    cache_key = get_replies_cache_key(topic_id)
    replies = topic.reply_set.order_by("-created_at")
    cache.set(cache_key, replies, timeout=CACHE_TIME)
