from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class Role:
    def __init__(self, name):
        self.name = name


class User:
    is_authenticated = True  # ВАЖНО для DRF

    def __init__(self, role_name):
        self.role = Role(role_name)


class DonationMockViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/mock/donations/'

    def test_user_cannot_get(self):
        self.client.force_authenticate(user=User('user'))
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_post(self):
        self.client.force_authenticate(user=User('user'))
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_moderator_can_get(self):
        self.client.force_authenticate(user=User('moderator'))
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_moderator_cannot_post(self):
        self.client.force_authenticate(user=User('moderator'))
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_get(self):
        self.client.force_authenticate(user=User('admin'))
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
