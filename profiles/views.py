import datetime
from datetime import date

import numpy as np
from django.http import JsonResponse
from django.utils.timezone import utc
from django.shortcuts import render, redirect, get_object_or_404

from florapedia.models import Plant
from posts.forms import PostModelForm
from posts.models import Post
from .models import Profile, Relationship
from .forms import ProfileModelForm, customForm
from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model

User = get_user_model()
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from flowerrecognising.CNN.DNNFlowers import predict
from PIL import Image


# Create your views here.

@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    myposts = Post.objects.filter(author=profile)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    form2 = customForm(request.POST or None, request.FILES or None , instance=profile)
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    for x in myposts:
        var =(now-x.date_of_last_watering).days
        if(var < 0):
            x.days_without_water = var  +1
        else:
            x.days_without_water = var+1

    confirm = False
    context = {
        'myposts': myposts,
        'profile': profile,
        'form': form,
        'form2': form2,
        'confirm': confirm,
    }

    if request.method == 'POST':
        print("t12")
        if form.is_valid():
            print("chek32")
            print(form)
            form.save()
            profile.save()
            confirm = True

    return render(request, 'profiles/myprofile.html', context)


@login_required
def watering_post(request):
    user = request.user

    if request.method == 'POST':
        print("wateringdjango")
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)
        post_obj.date_of_last_watering = date.today() - datetime.timedelta(days=1)
        post_obj.save()
    return redirect('profiles:my-profile-view')

@login_required
def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invatations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True

    context = {
        'qs': results,
        'is_empty': is_empty,
    }

    return render(request, 'profiles/my_invites.html', context)


@login_required
def accept_invatation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('profiles:my-invites-view')


@login_required
def reject_invatation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my-invites-view')


@login_required
def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {'qs': qs}

    return render(request, 'profiles/to_invite_list.html', context)


@login_required
def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {'qs': qs}

    return render(request, 'profiles/profile_list.html', context)


@login_required
def friends_list_view(request):
    user = request.user
    qs = Profile.objects.get_friends_manager(user)

    context = {'qs': qs}

    return render(request, 'profiles/my_friends_list.html', context)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    '''
    View for user detail page
    :return context: posts - all posts of user, len_posts - number of users posts , rel_receiver - list of users which got a invatation from current user,
    rel_sender - list of users which send a invatation to current user
    '''
    model = Profile
    template_name = 'profiles/detail.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
        return context


class ProfileListView(LoginRequiredMixin, ListView):
    '''
    View for list of all users
    :return qs: List of all users
    :return context: is_empty - boolean wich check if some users are avaible ,rel_receiver - list of users which got a invatation from current user,
    rel_sender - list of users which send a invatation to current user
    '''
    model = Profile
    template_name = 'profiles/profile_list.html'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context


@login_required
def send_invatation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')


@login_required
def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')

@login_required
def search_view(request):
    context={}
    if request.method == "GET":
        search_query= request.GET.get("q")
        if  len(search_query) > 0:
            search_results_profiles = Profile.objects.filter(
                Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query))
            search_results_posts = Post.objects.filter(Q(plant_name__icontains=search_query))
            search_results_plants = Plant.objects.filter(Q(plant_name__icontains=search_query))

    context['profiles_list']=search_results_profiles
    context['posts_list'] = search_results_posts
    context['plants_list'] = search_results_plants


    return render(request,"profiles/search_results.html",context )
