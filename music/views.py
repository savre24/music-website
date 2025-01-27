from django.shortcuts import render, get_object_or_404
from .models import Album, Music, Category, AdSettings

def get_ad_settings():
    """Fetch the AdSense codes (if available)"""
    return AdSettings.objects.first()

def home(request):
    """Homepage showing all albums and categories"""
    albums = Album.objects.all()
    categories = Category.objects.all()
    ads = get_ad_settings()  # Get ads from the database
    return render(request, 'home.html', {'albums': albums, 'categories': categories, 'ads': ads})

def album_detail(request, album_id):
    """View to display album details and tracks"""
    album = get_object_or_404(Album, id=album_id)
    tracks = Music.objects.filter(album=album)
    ads = get_ad_settings()
    return render(request, 'album_detail.html', {'album': album, 'tracks': tracks, 'ads': ads})

def track_detail(request, track_id):
    """View to display track details"""
    track = get_object_or_404(Music, id=track_id)
    album_tracks = track.album.tracks.exclude(id=track.id) if track.album else []
    ads = get_ad_settings()
    return render(request, 'track_detail.html', {'track': track, 'album_tracks': album_tracks, 'ads': ads})

def category_detail(request, category_id):
    """View to display albums under a specific category"""
    category = get_object_or_404(Category, id=category_id)
    albums = Album.objects.filter(category=category)
    ads = get_ad_settings()
    return render(request, 'category_detail.html', {'category': category, 'albums': albums, 'ads': ads})

