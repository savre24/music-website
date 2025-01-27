import os
import zipfile
from django.db import models
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.text import slugify


class Category(models.Model):
    """Album Category (e.g., Malayalam, Tamil, Hindi, Telugu)"""
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True, help_text="Upload a category image")

    def __str__(self):
        return self.name


class Album(models.Model):
    """Music Album"""
    title = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="albums")
    cover_image = models.ImageField(upload_to='album_covers/', blank=True, null=True, help_text="Upload an album cover")
    zip_file = models.FileField(upload_to='album_zips/', blank=True, null=True, help_text="Upload a ZIP file containing MP3s")

    def __str__(self):
        return self.title

    def extract_zip(self):
        """Extracts ZIP file and creates Music objects for each MP3 inside."""
        if self.zip_file:
            zip_path = self.zip_file.path
            album_folder = f"music_files/{slugify(self.title)}/"

            # Ensure the album folder exists
            if not default_storage.exists(album_folder):
                os.makedirs(default_storage.path(album_folder), exist_ok=True)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file_name in zip_ref.namelist():
                    if file_name.lower().endswith('.mp3'):  # Extract MP3 files only
                        file_content = zip_ref.read(file_name)
                        new_file_name = os.path.join(album_folder, os.path.basename(file_name))

                        # Save extracted MP3 file
                        saved_path = default_storage.save(new_file_name, ContentFile(file_content))

                        # Avoid duplicate tracks
                        if not Music.objects.filter(title=os.path.splitext(os.path.basename(file_name))[0], album=self).exists():
                            Music.objects.create(
                                title=os.path.splitext(os.path.basename(file_name))[0],
                                album=self,
                                file=saved_path
                            )

    def save(self, *args, **kwargs):
        """Override save method to extract ZIP after saving"""
        super().save(*args, **kwargs)  # Save album first
        if self.zip_file:
            self.extract_zip()  # Extract MP3s if ZIP is uploaded

        # Auto-set cover image if missing
        if not self.cover_image and self.tracks.exists():
            first_track = self.tracks.first()
            if first_track.cover_image:
                self.cover_image = first_track.cover_image
                super().save(update_fields=['cover_image'])


class Music(models.Model):
    """Individual Music Tracks"""
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, default="Unknown Artist")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="tracks", blank=True, null=True)
    file = models.FileField(upload_to='music_files/', help_text="Upload MP3 files")
    cover_image = models.ImageField(upload_to='music_covers/', blank=True, null=True, help_text="Upload an image for the track")

    def __str__(self):
        return self.title


class AdSettings(models.Model):
    """Model to store Google AdSense codes dynamically"""
    header_ad = models.TextField(blank=True, null=True, help_text="AdSense code for Header")
    footer_ad = models.TextField(blank=True, null=True, help_text="AdSense code for Footer")
    between_tracks_ad = models.TextField(blank=True, null=True, help_text="AdSense code between album tracks")

    def __str__(self):
        return "Google AdSense Settings"

    class Meta:
        verbose_name = "AdSense Setting"
        verbose_name_plural = "AdSense Settings"

