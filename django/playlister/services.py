import django
import django.db.models as db
from . import models


class PlaylistQuerySet(db.QuerySet):

    def as_simple_with_songs(self):
        return self.annotate(songs=db.F('entries__song'))


class PlaylistManager(db.manager.BaseManager.from_queryset(PlaylistQuerySet)):
    pass


class PlaylistEntryManager(db.Manager):

    def create(self, *args, **kwargs):
        super().create(*args, **kwargs)
