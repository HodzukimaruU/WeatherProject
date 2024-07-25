from django.test import TestCase
from django.urls import reverse
from .models import SearchHistory


class WeatherAppTests(TestCase):

    def setUp(self):
        self.client = self.client
        self.create_search_history()

    def create_search_history(self):
        SearchHistory.objects.create(city="Moscow")

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/index.html')

    def test_history_view(self):
        response = self.client.get(reverse('history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/history.html')
        self.assertContains(response, "Moscow")

    def test_autocomplete_view(self):
        response = self.client.get(reverse('autocomplete') + '?q=Mo')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, ['Moscow'])

    def test_city_stats_view(self):
        response = self.client.get(reverse('city_stats'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/city_stats.html')
    
    def test_repeat_search_view(self):
        response = self.client.get(reverse('repeat_search', args=['Moscow']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/repeat_search.html')
