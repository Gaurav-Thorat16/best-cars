from django.test import TestCase
from django.urls import reverse


class StaticPageTests(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Find the car that")
        self.assertContains(response, "fits your life.")

    def test_about_page(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A better way to buy")
        self.assertContains(response, "your next car.")

    def test_contact_page_shows_static_details(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "hello@bestcars.example")
