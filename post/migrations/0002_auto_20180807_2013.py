# Generated by Django 2.1 on 2018-08-07 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postmodel',
            options={'ordering': ['-created_at']},
        ),
    ]
