# Generated by Django 2.1 on 2018-09-09 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_profile', '0004_auto_20180826_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextramodel',
            name='follower',
            field=models.ManyToManyField(blank=True, related_name='is_following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userextramodel',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userextramodel', to=settings.AUTH_USER_MODEL),
        ),
    ]