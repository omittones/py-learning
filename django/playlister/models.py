from django.db import models
from . import services


def DefaultCharField(max_length=100, **kwargs):
    kwargs['null'] = kwargs.get('null', False)
    kwargs['blank'] = kwargs.get('blank', False)
    return models.CharField(max_length=max_length, **kwargs)


class SaveReturnsSelfMixin():

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return self


class Playlist(SaveReturnsSelfMixin, models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = DefaultCharField()
    source = DefaultCharField()
    source_specific_id = DefaultCharField(max_length=2000, blank=True, null=True)
    entries = None

    def __str__(self):
        return f"Playlist '{self.name}'"

    objects: services.PlaylistManager = services.PlaylistManager()

    def describe(self):
        songs = getattr(self, '_description', None)
        if songs is None:
            songs = self.entries.filter(order__lte=2).order_by('order').select_related('song')
        return ', '.join(map(lambda e: f'{e.song.artist} - {e.song.title}', songs))

    def add_songs(self, *songs):
        for song in songs:
            entry = PlaylistEntry(song=song, playlist=self)
            entry.save()


class PlaylistEntry(SaveReturnsSelfMixin, models.Model):

    id = models.AutoField(primary_key=True, auto_created=True)
    order = models.IntegerField(blank=False, null=False)
    song = models.ForeignKey(
        to='playlister.Song', on_delete=models.CASCADE, related_name='playlist_entries')
    playlist = models.ForeignKey(
        to='playlister.Playlist', on_delete=models.CASCADE, related_name='entries')

    class Meta():
        verbose_name = 'Playlist entry'
        verbose_name_plural = 'Playlist entries'

    objects = services.PlaylistEntryManager()

    # pylint: disable=no-member
    def __str__(self):
        self._song_artist = getattr(self, '_song_artist', self.song.artist)
        self._song_title = getattr(self, '_song_title', self.song.title)
        return f'{self.order}. {self._song_artist} - {self._song_title}'

    def order_key(self):
        return self.order

    def delete(self, *args, **kwargs):
        entries = self.playlist.entries.all()
        entries = [e for e in sorted(
            entries, key=PlaylistEntry.order_key) if e.id != self.id]
        for i, e in enumerate(entries):
            e.order = i
            super(PlaylistEntry, e).save()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        entries = self.playlist.entries.all()
        if self.order is None or kwargs.get('force_insert', False):
            self.order = max(map(PlaylistEntry.order_key, entries), default=-1)
            self.order += 1
        else:
            for i, e in enumerate(sorted(entries, key=PlaylistEntry.order_key)):
                e.order = i
                super(PlaylistEntry, e).save()
        super().save(*args, **kwargs)
        return self


class Song(SaveReturnsSelfMixin, models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    artist = DefaultCharField()
    album = DefaultCharField()
    title = DefaultCharField()

    def __str__(self):
        return f"{self.artist} - {self.title}"


class SongSource(SaveReturnsSelfMixin, models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    song = models.ForeignKey(to='playlister.Song',
                             on_delete=models.SET_NULL, blank=True, null=True)
    source = DefaultCharField()
    source_specific_id = DefaultCharField(
        max_length=2000, blank=False, null=False)
