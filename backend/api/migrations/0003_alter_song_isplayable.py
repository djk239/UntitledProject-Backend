# Generated by Django 4.2.13 on 2024-06-07 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_song_isplayable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='isPlayable',
            field=models.BooleanField(default=False),
        ),
    ]