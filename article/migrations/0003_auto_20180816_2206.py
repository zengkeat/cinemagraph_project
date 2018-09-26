# Generated by Django 2.1 on 2018-08-16 14:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_articlemodel_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlemodel',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='article', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['gif', 'png', 'jpg', 'jpeg', 'mp4'])]),
        ),
    ]
