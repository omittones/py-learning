from django.test import TestCase, tag
from . import models


@tag('smoke', 'playlister')
class SmokeTests(TestCase):

    def setUp(self):
        self.first = models.Playlist(name='Test playlist 0001').save()
        self.second = models.Playlist(name='Test playlist 0002').save()
        self.songs = [models.Song(artist='Artist 1', album='Mixes', title='Song 1').save(),
                      models.Song(artist='Artist 2', album='Mixes', title='Song 2').save()]
        self.second.add_songs(*self.songs)

    def test_queryset_works(self):
        self.assertEqual(2, models.Playlist.objects.all().count())

        query = models.Playlist.objects.all().as_simple_with_songs()

        items = list(query)
        self.assertEqual(2, len(items))
        self.assertEqual('Test playlist 0001', items[0].name)
        self.assertEqual('Test playlist 0002', items[1].name)

    def test_home_page(self):
        self.assertEqual(200, self.client.get('/').status_code)

    def test_playlists_show_on_homepage(self):
        response = self.client.get('/')
        self.assertContains(response, 'Test playlist 0001')
        self.assertContains(response, 'Test playlist 0002')
