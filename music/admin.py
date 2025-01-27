from django.contrib import admin
from .models import Category, Album

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    list_filter = ('category',)
    search_fields = ('title',)


from django.contrib import admin
from .models import AdSettings

@admin.register(AdSettings)
class AdSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'header_ad', 'footer_ad', 'between_tracks_ad')
