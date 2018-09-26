# Generated by Django 2.1 on 2018-08-16 13:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlemodel',
            name='file',
            field=models.FileField(blank=True, upload_to='article', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['gif', 'png', 'jpg', 'jpeg', 'mp4'])]),
        ),
    ]
