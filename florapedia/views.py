from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from florapedia.models import Plant
from profiles.models import Profile


@login_required
def main_florapedia_view(request):

    qs = Plant.objects.all()
    profile = Profile.objects.get(user=request.user)


    context = {
        'qs': qs,
        'profile': profile,
    }

    return render(request, 'florapedia/main.html', context)
