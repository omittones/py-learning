import django
import django.db.models as db
import typing
from . import models
from abc import ABC, abstractmethod


class PlaylistViewModel():
    def __init__(self, *args, **kwargs):
        playlist = args[0] if args else None
        self.id = playlist.id if playlist else kwargs.get('id', None)
        self.name = playlist.name if playlist else kwargs.get('name', None)
        if playlist is not None:
            self.description = playlist.describe()
        else:
            self.description = kwargs.get('description', '')


class DataProvider(ABC):

    @staticmethod
    def resolve(source) -> 'DataProvider':
        services = {
            'local': LocalDataProvider(),
            'deezer': DeezerDataProvider()
        }
        return services.get(source, services['local'])

    @abstractmethod
    def playlist_overview(self) -> typing.Iterable[PlaylistViewModel]:
        pass


class DeezerDataProvider(DataProvider):

    def playlist_overview(self):
        if False:
            yield None
        # query = models.Playlist.objects.all().with_description()
        # for item in query:
        #     yield PlaylistViewModel(item)


class LocalDataProvider(DataProvider):

    def playlist_overview(self):
        query = models.Playlist.objects.all().with_description()
        for item in query:
            yield PlaylistViewModel(item)


class PlaylistQuerySet(db.QuerySet):

    def where_empty(self):
        return self.annotate(nm_entries=db.Count('entries')).filter(nm_entries__exact=0)

    def with_description(self):
        #pylint: disable=no-member
        top3entries = models.PlaylistEntry.objects.filter(order__lte=2).order_by('order')
        return self.prefetch_related(
            db.Prefetch('entries', top3entries, '_description'), '_description__song')


class PlaylistManager(db.manager.BaseManager.from_queryset(PlaylistQuerySet)):

    def all(self) -> PlaylistQuerySet:
        return super().all()
