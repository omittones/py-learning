def setup_django():
    import myproject.settings
    import django
    from django.conf import settings
    settings.configure(
        DATABASES=myproject.settings.DATABASES,
        INSTALLED_APPS=myproject.settings.INSTALLED_APPS,
        DEBUG=True
    )
    django.setup()

# pylint: disable=unused-variable
# pylint: disable=no-member


def sql(queryset):
    query = getattr(queryset, 'query', queryset)
    print(query, '\n')


def exc(queryset):
    list(queryset)


def try_to_join():
    from playlister import models
    from django.db.models.sql.query import LOUTER, INNER, Query, Join
    from django.db.models.sql.datastructures import BaseTable
    #from django.db.models.sql import Query, Join

    class JoinCondition():
        def __init__(self, *args):
            self.join_columns = args

        def get_joining_columns(self):
            return self.join_columns

        def get_extra_restriction(self, *args, **kwargs):
            return None

    # join
    qset = models.Playlist.objects.filter(name__exact='a')
    query: Query = qset.query

    condition = JoinCondition(
        (models.Playlist._meta.get_field('name').column,
         models.Song._meta.get_field('title').column)
    )

    parent_alias = query.table_alias(models.Playlist._meta.db_table)[0]
    query.join(Join(
        table_name=models.Song._meta.db_table,
        table_alias=None,
        parent_alias=parent_alias,
        join_type=LOUTER,
        join_field=condition,
        nullable=True
    ))

    sql(query)


def main():
    from playlister import models
    from django.db import connection
    from django.db.models import F, Count, Q, FilteredRelation
    import django.db.models.functions as DbF
    from django.db.models.manager import BaseManager

    playlists: BaseManager = models.Playlist.objects
    songs: BaseManager = models.Song.objects

    # slicing returns LimiterQuerySet, pure indexing does not
    first_playlist = playlists.all()[:1]

    # where name like '%Seeded%'
    sql(playlists.filter(name__contains='Seeded').all())

    # where any entry has a song of Amon Tobin
    sql(playlists.filter(entries__song__artist__exact='Amon Tobin').all())

    # where song artist is same as title
    sql(songs.filter(artist__exact=F('title')))

    # where artist start with title first char
    sql(songs.filter(artist__startswith=DbF.Substr(F('title'), 1, 1)))

    # where artist first char same as title first char
    sql(songs
        .annotate(afc=DbF.Substr(F('artist'), 1, 1))
        .filter(afc__exact=DbF.Substr(F('title'), 1, 1)))

    # group by first letter
    sql(songs
        .values(first_char=DbF.Substr(F('artist'), 1, 1))
        .annotate(nm_songs=Count(F('id'))))

    # id in array
    sql(songs
        .filter(id__in=[1, 2, 3]))

    # union
    sql(
        playlists
        .values('name', 'name')
        .union(songs.values('title', 'artist'))
    )

    try_to_join()

    # print all queries executed on database connection
    [print(i['sql'], '\n') for i in connection.queries]
    return


if __name__ == '__main__':
    setup_django()
    main()
