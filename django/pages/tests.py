from django.test import TestCase, tag


@tag('smoke', 'pages')
class SmokeTests(TestCase):

    def test_pages_home(self):
        response = self.client.get('/pages/')
        self.assertEqual(200, response.status_code)

    def test_about_page(self):
        response = self.client.get('/pages/about/')
        self.assertEqual(200, response.status_code)
