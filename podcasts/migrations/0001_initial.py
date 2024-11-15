# Generated by Django 4.2.10 on 2024-05-14 05:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spotify_id', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('image', models.CharField(max_length=200, null=True)),
                ('publisher', models.CharField(max_length=200, null=True)),
                ('users', models.ManyToManyField(related_name='podcasts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
