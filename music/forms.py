from django import forms
from .models import Music

class MusicUploadForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['title', 'artist', 'file']
