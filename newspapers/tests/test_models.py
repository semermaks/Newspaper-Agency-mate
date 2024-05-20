from django.test import TestCase
from newspapers.models import Topic, Redactor, Newspaper, ActivateToken


class TopicModelTest(TestCase):
    def test_topic_creation(self):
        topic = Topic.objects.create(title="Test Topic")
        self.assertEqual(topic.title, "Test Topic")


class RedactorModelTest(TestCase):
    def test_redactor_creation(self):
        redactor = Redactor.objects.create(username="test_redactor", years_of_experience=3)
        self.assertEqual(redactor.username, "test_redactor")
        self.assertEqual(redactor.years_of_experience, 3)


class NewspaperModelTest(TestCase):
    def test_newspaper_creation(self):
        topic = Topic.objects.create(title="Test Topic")
        redactor = Redactor.objects.create(username="test_redactor", years_of_experience=3)
        newspaper = Newspaper.objects.create(title="Test Newspaper", content="Test content", topic=topic)
        newspaper.redactor.add(redactor)
        self.assertEqual(newspaper.title, "Test Newspaper")
        self.assertEqual(newspaper.content, "Test content")
        self.assertEqual(newspaper.topic, topic)
        self.assertIn(redactor, newspaper.redactor.all())


class ActivateTokenModelTest(TestCase):
    def test_token_creation(self):
        redactor = Redactor.objects.create(username="test_redactor", years_of_experience=3)
        token = ActivateToken.objects.create(user=redactor)
        self.assertTrue(token.verify_token())
