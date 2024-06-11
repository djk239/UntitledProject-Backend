from django.contrib import admin
from .models import Song

class SongAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'artist', 'audio_link', 'isPlayable')
    fields = ('id', 'title', 'artist', 'audio_link', 'isPlayable')
    readonly_fields = ('id',)  # Make the id field read-only

admin.site.register(Song, SongAdmin)