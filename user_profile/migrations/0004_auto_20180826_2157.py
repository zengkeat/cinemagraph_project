# Generated by Django 2.1 on 2018-08-26 13:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_auto_20180803_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextramodel',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]