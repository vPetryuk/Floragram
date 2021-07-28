import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
from .models import Discussion, Message, last_50_messages


def index(request):
    return render(request, 'chat/index.html', {})

@login_required
def room(request, room_name):
    messages = last_50_messages(room_name)
    print(messages)


    return render(request, 'chat/room.html', {
        'messages': messages,
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
        'username_f': request.user.username,
    })
