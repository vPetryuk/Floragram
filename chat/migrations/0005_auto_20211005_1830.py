# Generated by Django 3.1.8 on 2021-10-05 15:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20211005_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussion',
            name='image',
            field=models.ImageField(default='/static/images/discdef.jpg', upload_to='discussion_image', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])]),
        ),
    ]