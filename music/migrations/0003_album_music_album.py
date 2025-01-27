# Generated by Django 5.1.5 on 2025-01-26 16:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_remove_music_uploaded_at_music_cover_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('cover_image', models.ImageField(blank=True, help_text='Upload an album cover', null=True, upload_to='album_covers/')),
            ],
        ),
        migrations.AddField(
            model_name='music',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to='music.album'),
        ),
    ]
