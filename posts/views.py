from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from florapedia.models import Plant
from flowerrecognising.CNN.DNNFlowers import predict
from .models import Post, Like
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
    qs = Post.objects.all()
    profile = Profile.objects.get(user=request.user)

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
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'

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
            image = Image.open(form2.instance.image)
            print(predict(image))
            form2.instance.intended_plant_name =predict(image)
            print(form2.instance.intended_plant_name)
            form2.save()
            confirm2 = True
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
    plant = Plant.objects.get(plant_name=post.intended_plant_name)
    form = PostModelNameForm(request.POST or None, request.FILES or None,instance=post )

    confirm = False



    if request.method == 'POST':
        if form.is_valid():

            form.save()
            confirm = True
            return redirect('posts:post-detail', form.instance.pk)

    context = {
        'post':post,
        'plant': plant,
        'profile': profile,

        'form': form,

        'confirm': confirm,
    }

    return render(request, 'posts/recognising.html', context)

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/plant_detail.html'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)
        plant = Plant.objects.get(plant_name=post.intended_plant_name)
        context['post'] = post
        context['plant'] = plant
        return context

class PostDeleteView(LoginRequiredMixin, DeleteView):
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
    form_class = PostModelForm
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:main-post-view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "You need to be the author of the post in order to update it")
            return super().form_invalid(form)

