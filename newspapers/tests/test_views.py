from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from newspapers.models import Redactor


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@example.com',
            password='password'
        )
        self.redactor = Redactor.objects.create(
            username='redactor',
            years_of_experience=5
        )

    def test_newspaper_create_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse(
            'newspapers:newspapers-create'),
            {'title': 'Test',
             'content': 'Test Content',
             'topic': 1}
        )
        self.assertEqual(response.status_code, 200)

    def test_redactor_profile_view(self):
        self.client.force_login(self.redactor)
        response = self.client.get(reverse(
            'newspapers:redactor-list')
        )
        self.assertEqual(response.status_code, 200)
