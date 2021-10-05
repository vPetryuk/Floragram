import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import DeleteView, UpdateView, DetailView
import random
import string
from django.utils.text import slugify
from profiles.models import Profile
from .forms import DiscussionModelForm
from .models import Discussion, Message, last_50_messages
from django.contrib import messages

def index(request):
    return render(request, 'chat/index.html', {})

@login_required
def room(request, slug):
    messages = last_50_messages(slug)
    context={'messages': messages,
            'room_name_json': mark_safe(json.dumps(slug)),
            'username': mark_safe(json.dumps(request.user.username)),
            'username_f': request.user.username,}


    return render(request, 'chat/room.html', context)

@login_required
def discussion_list_view(request):
    '''
    View for forum page which shows all discussions
    :param request:
    :return page: Page forum.html
    :return context: context ( qs - list of all discussion object , profile - profile of current user)

    '''
    qs = Discussion.objects.all()


    profile = Profile.objects.get(user=request.user)


    context = {
        'qs': qs[::-1],
        'profile': profile,

    }

    return render(request, 'chat/forum.html', context)

class DiscussionDeleteView(LoginRequiredMixin, DeleteView):
    '''
    Redirect to page to confirm deleting discussion
    :param pk: Primary key of discussion which needs to be delete
    '''
    model = Discussion
    template_name = 'chat/confirm_delete.html'
    success_url = reverse_lazy('chat:main-chat-view')



    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Discussion.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You need to be the author of the discussion in order to delete it')
        return obj


class DiscussionUpdateView(LoginRequiredMixin, UpdateView):
    '''
    Redirect to page to update discussion
    :param pk: Primary key of discussion which needs to be updated
    '''
    form_class = DiscussionModelForm
    model = Discussion
    template_name = 'chat/update.html'
    success_url = reverse_lazy('chat:main-chat-view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:

            return super().form_valid(form)
        else:
            form.add_error(None, "You need to be the author of the post in order to update it")
            return super().form_invalid(form)

# class DiscussionDetailView(LoginRequiredMixin, DetailView):
#     '''
#     View for detail room page
#     :return context: discussion - current room taken by pk
#
#     '''
#     model = Discussion
#     template_name = 'chat/room.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         slug = self.kwargs.get('slug')
#         discussion = Discussion.objects.get(slug=slug)
#         context['discussion'] = discussion
#         return context

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.Discussion_name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

@login_required
def add_discussion_view(request):
    profile = Profile.objects.get(user=request.user)
    form = DiscussionModelForm(request.POST or None, request.FILES or None, )


    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = profile
            form.instance.slug =unique_slug_generator(form.instance)
            form.save()
            return redirect('chat:room', form.instance.Discussion_name)

    context = {
        'profile': profile,
        'form': form,
    }

    return render(request, 'chat/add_new_discussion.html', context)
