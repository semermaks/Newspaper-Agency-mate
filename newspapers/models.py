from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string


class Topic(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title}"


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(default=1)

    class Meta:
        ordering = ["years_of_experience", "username"]
        verbose_name = "redactor"
        verbose_name_plural = "redactors"

    def __str__(self):
        return (f"{self.username} ({self.first_name} {self.last_name}): "
                f"{self.years_of_experience} years")

    def get_absolute_url(self):
        return reverse("newspapers:redactor-detail", kwargs={"pk": self.pk})


class Newspaper(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True, blank=True)
    main_img = models.ImageField(upload_to='images/', default='images/default.jpg')

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="newspapers")
    redactor = models.ManyToManyField(Redactor, related_name="newspapers")

    class Meta:
        ordering = ["-published_date"]

    def __str__(self):
        return f"{self.title}: {self.content} ({self.published_date})"


class AbstractToken(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=64, unique=True, default=None, blank=True)
    user = models.ForeignKey(Redactor, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def verify_token(self, days: int = 1) -> bool:
        validate_exp = timezone.localtime(self.create_at) > timezone.now() - timezone.timedelta(days=days)
        return validate_exp

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(length=64)
        super().save(*args, **kwargs)


class ActivateToken(AbstractToken):
    class Meta:
        verbose_name_plural = "Activation tokens"

    def __str__(self):
        return f"{self.user}'s token activate: {self.token}"
