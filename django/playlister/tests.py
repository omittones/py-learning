from django.test import TestCase, tag
from . import models


@tag('smoke', 'playlister')
class SmokeTests(TestCase):

    def setUp(self):
        self.first = models.Playlist(name='Test playlist 0001').save()
        self.second = models.Playlist(name='Test playlist 0002').save()
        self.songs = [models.Song(artist='Artist 1', album='Mixes', title='Song 1').save(),
                      models.Song(artist='Artist 2', album='Mixes', title='Song 2').save(),
                      models.Song(artist='Artist 3', album='Mixes', title='Song 3').save(),
                      models.Song(artist='Artist 4', album='Mixes', title='Song 4').save(),
                      models.Song(artist='Artist 5', album='Mixes', title='Song 5').save()]
        self.first.add_songs(*self.songs[2:])
        self.second.add_songs(*self.songs)

    def test_description(self):
        items = list(models.Playlist.objects.all())
        self.assertEqual('Artist 3 - Song 3, Artist 4 - Song 4, Artist 5 - Song 5', items[0].describe())
        self.assertEqual('Artist 1 - Song 1, Artist 2 - Song 2, Artist 3 - Song 3', items[1].describe())

    def test_prefetching_description(self):
        self.assertEqual(2, models.Playlist.objects.all().count())
        query = models.Playlist.objects.all().with_description()
        items = list(query)
        with self.assertNumQueries(0):
            self.assertEqual(2, len(items))
            self.assertEqual('Test playlist 0001', items[0].name)
            self.assertEqual('Test playlist 0002', items[1].name)
            self.assertEqual('Artist 3 - Song 3, Artist 4 - Song 4, Artist 5 - Song 5', items[0].describe())
            self.assertEqual('Artist 1 - Song 1, Artist 2 - Song 2, Artist 3 - Song 3', items[1].describe())
            for pl in items:
                self.assertEqual(3, len(pl._description))

    def test_home_page(self):
        self.assertEqual(200, self.client.get('/').status_code)

    def test_playlists_show_on_homepage(self):
        response = self.client.get('/')
        self.assertContains(response, 'Test playlist 0001')
        self.assertContains(response, 'Test playlist 0002')
        self.assertContains(response, 'Artist 3 - Song 3, Artist 4 - Song 4, Artist 5 - Song 5')
        self.assertContains(response, 'Artist 1 - Song 1, Artist 2 - Song 2, Artist 3 - Song 3')
