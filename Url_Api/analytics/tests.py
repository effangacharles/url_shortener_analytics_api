from django.test import TestCase
from django.urls import reverse
from shortener.models import URL


class AnalyticsDashboardTests(TestCase):
    def test_analytics_index_renders(self):
        response = self.client.get(reverse('analytics_index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Analytics Demo')

    def test_dashboard_renders(self):
        url = URL.objects.create(long_url='https://example.com')

        response = self.client.get(reverse('analytics_dashboard', kwargs={'short_code': url.short_code}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Analytics Dashboard')
        self.assertContains(response, url.long_url)
