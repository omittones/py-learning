from django.db import models


def DefaultCharField(max_length=100, **kwargs):
    kwargs['null'] = kwargs.get('null', False)
    kwargs['blank'] = kwargs.get('blank', False)
    return models.CharField(max_length=max_length, **kwargs)


class Playlist(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = DefaultCharField()
    source = DefaultCharField()
    source_specific_id = DefaultCharField(
        max_length=2000, blank=True, null=True)

    def __str__(self):
        return f"Playlist '{self.name}'"


class PlaylistEntry(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    order = models.IntegerField(blank=False, null=False)
    song = models.ForeignKey(
        to='playlister.Song', on_delete=models.CASCADE, related_name='playlist_entries')
    playlist = models.ForeignKey(
        to='playlister.Playlist', on_delete=models.CASCADE, related_name='entries')


class Song(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    artist = DefaultCharField()
    album = DefaultCharField()
    title = DefaultCharField()

    def __str__(self):
        return f"{self.artist} - {self.title}"


class SongSource(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    song = models.ForeignKey(to='playlister.Song',
                             on_delete=models.SET_NULL, blank=True, null=True)
    source = DefaultCharField()
    source_specific_id = DefaultCharField(
        max_length=2000, blank=False, null=False)
