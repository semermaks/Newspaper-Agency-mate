from django.contrib.auth.models import AbstractUser
from django.db import models

from Newspaper_Agency_mate import settings


class Topic(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title}"


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField()

    class Meta:
        ordering = ["years_of_experience"]
        verbose_name = "redactors"
        verbose_name_plural = "redactors"

    def __str__(self):
        return (f"{self.username} ({self.first_name} {self.last_name}): "
                f"{self.years_of_experience} years")


class Newspaper(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    published_date = models.DateTimeField()

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="newspapers")
    publishers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="newspapers")

    class Meta:
        ordering = ["published_date"]

    def __str__(self):
        return f"{self.title}: {self.content} ({self.published_date})"
