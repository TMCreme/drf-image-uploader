from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from .models import User, AccountTier, UserImage
import base64


class APITests(SimpleTestCase):
    def test_root_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 404)

    def test_list_images_without_auth(self):
        response = self.client.get("/home/api-list-images/")
        self.assertEqual(response.status_code, 401)


class UserTestClass(TestCase):
    def setUp(self) -> None:
        User.objects.create(
            username="test1",
            password="password12",
            account_tier=AccountTier.objects.get(name="BASIC")
        )

    def test_user_login(self):
        response = self.client.login(
            username="test1", password="password12"
            )
        self.assertEqual(response, True)

    def test_list_images_with_auth(self):
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(
                'test1:password12'.encode('utf8')).decode('utf8'),
        }
        response = self.client.get(
            "/home/api-list-images/", **auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_list_thumbnail_with_auth(self):
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(
                'test1:password12'.encode('utf8')).decode('utf8'),
        }
        response = self.client.get(
            "/home/api-list-image-thumbnail/", **auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_users_with_account_tier(self):
        user1 = User.objects.get(username="test1")
        self.assertEqual(user1.username, "test1")



# Create your tests here.
