from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth import get_user_model

from profiles.models import Profile

User = get_user_model()


def last_50_messages(slug):
    discussion = Discussion.objects.get(slug=slug)
    return discussion.messages.order_by('-timestamp').all().reverse()[:50]

class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username



class Discussion(models.Model):
    image = models.ImageField(upload_to='discussion_image', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],default="/preloaded_img/discdef.jpg")
    Discussion_name = models.TextField()
    participants = models.ManyToManyField(
        User, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True,)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = content = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='discussion', blank=True, default=1)
    def __str__(self):
        return "{}".format(self.pk)
