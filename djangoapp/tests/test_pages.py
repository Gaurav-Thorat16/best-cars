from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class StaticPageTests(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Find the car that")
        self.assertContains(response, "fits your life.")

    def test_home_page_filters_dealers_by_state(self):
        response = self.client.get(reverse("home"), {"state": "Kansas"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Best Cars Wichita")
        self.assertNotContains(response, "Best Cars Downtown")

    def test_dealer_detail_shows_reviews(self):
        response = self.client.get("/dealer/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Best Cars Downtown")
        self.assertContains(response, "The team made the whole purchase clear and easy.")

    def test_post_review_page_shows_review_form(self):
        response = self.client.get("/dealer/1/review/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Best Cars Downtown")
        self.assertContains(response, "Submit review")

    def test_about_page(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A better way to buy")
        self.assertContains(response, "your next car.")

    def test_contact_page_shows_static_details(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "hello@bestcars.example")


class AuthenticationApiTests(TestCase):
    def test_register_logs_user_in(self):
        response = self.client.post(
            reverse("register_api"),
            data={"username": "driver", "password": "strong-pass-123"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["username"], "driver")
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_duplicate_username_returns_clear_error(self):
        User.objects.create_user(username="driver", password="strong-pass-123")
        response = self.client.post(
            reverse("register_api"),
            data={"username": "DRIVER", "password": "strong-pass-123"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["error"], "That username is already registered.")

    def test_login_and_logout(self):
        User.objects.create_user(username="driver", password="strong-pass-123")
        login_response = self.client.post(
            reverse("login_api"),
            data={"username": "driver", "password": "strong-pass-123"},
            content_type="application/json",
        )
        self.assertEqual(login_response.status_code, 200)
        logout_response = self.client.post(reverse("logout_api"))
        self.assertEqual(logout_response.status_code, 200)

    def test_home_page_hydrates_logged_in_username(self):
        User.objects.create_user(username="driver", password="strong-pass-123")
        self.client.login(username="driver", password="strong-pass-123")
        response = self.client.get(reverse("home"))
        self.assertContains(response, 'data-username="driver"')
