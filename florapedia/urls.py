from django.urls import path

from . import views
from .views import main_florapedia_view

app_name= 'florapedia'

urlpatterns = [

    path('', main_florapedia_view, name='main-florapedia-view'),

]
