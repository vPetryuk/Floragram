from django.contrib import admin
from .models import Post, Comment, Like, image_of_growth_stage

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(image_of_growth_stage)

