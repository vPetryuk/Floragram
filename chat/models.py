from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def last_50_messages(discussion_name):
    discussion = Discussion.objects.get(Discussion_name=discussion_name)
    return discussion.messages.order_by('-timestamp').all().reverse()[:50]

class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username



class Discussion(models.Model):
    image = models.ImageField(upload_to='discussion_image', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],blank=True)
    Discussion_name = models.TextField()
    participants = models.ManyToManyField(
        User, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True,)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.pk)
