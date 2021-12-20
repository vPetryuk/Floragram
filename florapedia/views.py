from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from florapedia.models import Plant
from profiles.models import Profile


@login_required
def main_florapedia_view(request):

    qs = Plant.objects.all().exclude(plant_name="Unknown")
    qsr = reversed(list(qs))
    profile = Profile.objects.get(user=request.user)


    context = {
        'qs': qsr,
        'profile': profile,
    }

    return render(request, 'florapedia/main.html', context)

class PlantDetailView(LoginRequiredMixin, DetailView):
    '''
    View for detail page
    :return context: post - current post taken by pk , plant - info about this type of plant taken from florapedia

    '''
    model = Plant
    template_name = 'florapedia/plant_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        plant = Plant.objects.get(pk=pk)
        context['plant'] = plant
        return context

@login_required
def plants_subcategory_list_view(request,subcategory):
    qs = Plant.objects.filter(subcategory=subcategory)
    context = {'qs': qs}
    return render(request, 'florapedia/main.html', context)

@login_required
def plants_category_list_view(request,category):
    qs = Plant.objects.filter(category=category)
    context = {'qs': qs}
    return render(request, 'florapedia/main.html', context)
