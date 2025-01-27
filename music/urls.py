from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home, album_detail, track_detail, category_detail  # ✅ Ensure all views are imported

urlpatterns = [
    path('', home, name='home'),  # Homepage showing all albums and categories
    path('album/<int:album_id>/', album_detail, name='album_detail'),
    path('track/<int:track_id>/', track_detail, name='track_detail'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),  # ✅ Fixed category route
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

