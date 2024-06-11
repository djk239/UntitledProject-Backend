from django.db import models



class Song(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    audio_link = models.URLField()
    isPlayable = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class Quiz(models.Model):
    title = models.CharField(max_length=100)
    songs = models.ManyToManyField(Song)


    def __str__(self):
        return self.title
    