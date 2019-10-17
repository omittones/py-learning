from . import models
import django
import django.db.models as db
import typing
import deezer
from abc import ABC, abstractmethod


class PlaylistViewModel():
    def __init__(self, *args, **kwargs):
        playlist = args[0] if args else None
        self.id = playlist.id if playlist else kwargs.get('id', None)
        self.name = playlist.name if playlist else kwargs.get('name', None)
        self.thumbnail_url = 'https://picsum.photos/128/128'
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

    @property
    def client(self):
        if not hasattr(self, '_client'):
            settings = models.DeezerSettings.objects.get()  # pylint: disable=no-member
            self._client = deezer.Client(app_id=settings.app_id,
                                         app_secred=settings.app_secret,
                                         access_token=settings.access_token,
                                         follow_next_links=True)
        return self._client

    def playlist_overview(self):
        for p in self.client.get_user_playlists('me'):
            model = PlaylistViewModel()
            model.id = p.id
            model.name = p.title
            model.description = f'Nm. tracks {p.nb_tracks}'
            model.thumbnail_url = p.picture_medium
            yield model


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
