from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model as user_model

from posts.models import Post, image_of_growth_stage

User = user_model()


# @receiver(pre_save, sender=Post)
# def pre_save_new_plant_image(sender, instance, **kwargs):
#     if not instance._state.adding:
#         print("tut")
#         h = image_of_growth_stage(plant_name=instance.plant_name , image=instance.image )
#         h.save()
#         instance.history = h
#         instance.save()
