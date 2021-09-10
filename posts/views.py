from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from florapedia.models import Plant
from flowerrecognising.CNN.DNNFlowers import predict, scientific_to_fine_percent, scientific_to_real
from .models import Post, Like, image_of_growth_stage
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm, PostModelNameForm
from django.views.generic import UpdateView, DeleteView, DetailView
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from PIL import Image


# Create your views here.

@login_required
def post_comment_create_and_list_view(request):
    '''
    View for main page which shows all posts
    :param request:
    :return page: Page main.html
    :return context: context ( qs - list of all posts object , profile - profile of current user, p_form - PostModelForm , c_form , CommentModelForm ,post_added = boolean)

    '''
    qs = Post.objects.exclude(plant_name="Plant")


    # initials
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_added = False

    profile = Profile.objects.get(user=request.user)

    if 'submit_p_form' in request.POST:
        print(request.POST)
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_added = True

    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()

    context = {
        'qs': qs,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
        'post_added': post_added,
    }

    return render(request, 'posts/main.html', context)


@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)
        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'
            post_obj.save()
            like.save()

        # data = {
        #     'value': like.value,
        #     'likes': post_obj.liked.all().count()
        # }
        # return JsonResponse(data, safe=False)
    return redirect('posts:main-post-view')


@login_required
def rec_confirm_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)
        post_obj.plant_name = post_obj.intended_plant_name
        post_obj.save()
        return redirect('posts:post-detail', post_id)


@login_required
def add_post_view(request):
    profile = Profile.objects.get(user=request.user)
    form2 = PostModelForm(request.POST or None, request.FILES or None, )
    confirm2 = False

    if request.method == 'POST':
        if form2.is_valid():
            form2.instance.author = profile
            form2.save()
            return redirect('posts:recognise-post-view')

    context = {

        'profile': profile,

        'form2': form2,

        'confirm2': confirm2,
    }

    return render(request, 'posts/add_new_post.html', context)



@login_required
def recognise_post_view(request):
    profile = Profile.objects.get(user=request.user)
    post = Post.objects.filter(author=profile).latest('created')
    #plant = Plant.objects.get(plant_name=post.intended_plant_name)
    form = PostModelNameForm(request.POST or None, request.FILES or None, instance=post)
    print(post.image)
    predictions = predict(Image.open(post.image))
    post.intended_plant_name=predictions[0][0]
    post.save()
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
            return redirect('posts:post-detail', form.instance.pk)




    context = {
        'post': post,
        'profile': profile,
        'form': form,
        'confirm': confirm,
        'prediction1':predictions[0][0],
        'prediction2': predictions[1][0],
        'prediction3': predictions[2][0],
        'prediction4': predictions[3][0],
        'prediction5': predictions[4][0],
        'probability2': scientific_to_fine_percent(predictions[1][1],predictions[1][1]),
        'probability3': scientific_to_fine_percent(predictions[2][1],predictions[1][1]),
        'probability4': scientific_to_fine_percent(predictions[3][1],predictions[1][1]),
        'probability5': scientific_to_fine_percent(predictions[4][1],predictions[1][1]),

    }
    return render(request, 'posts/recognising.html', context)


class PostDetailView(LoginRequiredMixin, DetailView):
    '''
    View for detail page
    :return context: post - current post taken by pk , plant - info about this type of plant taken from florapedia

    '''
    model = Post
    template_name = 'posts/plant_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)
        plant = Plant.objects.get(plant_name=post.plant_name)
        history = self.get_object().image_of_growth_stage()
        context['post'] = post
        context['plant'] = plant
        IsEmpty = True;
        if history:
            isEmpty = False;
            context['IsEmty'] = IsEmpty
            context['history'] = history

        return context


class PostDeleteView(LoginRequiredMixin, DeleteView):
    '''
    Redirect to page to confirm deleting post
    :param pk: Primary key of post which needs to be delete
    '''
    model = Post
    template_name = 'posts/confirm_delete.html'
    success_url = reverse_lazy('posts:main-post-view')

    # success_url = '/posts/'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You need to be the author of the post in order to delete it')
        return obj


class PostUpdateView(LoginRequiredMixin, UpdateView):
    '''
    Redirect to page to update post
    :param pk: Primary key of post which needs to be updated
    '''
    form_class = PostModelForm
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('profiles:my-profile-view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            h = image_of_growth_stage(plant_name=form.instance.plant_name, image=form.instance.image)
            h.save()

            form.instance.history.add(h)
            return super().form_valid(form)
        else:
            form.add_error(None, "You need to be the author of the post in order to update it")
            return super().form_invalid(form)
