# Generated by Django 2.1 on 2018-08-19 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentmodel',
            name='article',
        ),
        migrations.RemoveField(
            model_name='commentmodel',
            name='post',
        ),
    ]
