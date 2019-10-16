import django
import django.db.models as db
from . import models


class PlaylistQuerySet(db.QuerySet):

    def where_empty(self):
        return self.annotate(nm_entries=db.Count('entries')).filter(nm_entries__exact=0)

    def with_description(self):
        top3entries = models.PlaylistEntry.objects.filter(order__lte=2).order_by('order')
        return self.prefetch_related(
            db.Prefetch('entries', top3entries, '_description'), '_description__song')


class PlaylistManager(db.manager.BaseManager.from_queryset(PlaylistQuerySet)):

    def all(self) -> PlaylistQuerySet:
        return super().all()


class PlaylistEntryManager(db.Manager):

    def create(self, *args, **kwargs):
        super().create(*args, **kwargs)
