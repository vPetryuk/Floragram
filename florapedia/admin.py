from django.contrib import admin

# Register your models here.
from florapedia.models import Plant

from embed_video.admin import AdminVideoMixin


class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

admin.site.register(Plant, MyModelAdmin)
# admin.site.register(Plant)
