from django.urls import path


from .views import main_florapedia_view, PlantDetailView, plants_subcategory_list_view, plants_category_list_view

app_name= 'florapedia'

urlpatterns = [

    path('', main_florapedia_view, name='main-florapedia-view'),
    path('<pk>/detail/', PlantDetailView.as_view(), name='plant-detail'),
    path('plants-list/<str:subcategory>/', plants_subcategory_list_view, name='plants-list'),
    path('plants-category-list/<str:category>/', plants_category_list_view, name='plants-category-list'),
]
