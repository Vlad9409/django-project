from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Note(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200)
    text = models.TextField(verbose_name="Note text")
    reminder = models.DateTimeField(
        null=True, blank=True, verbose_name="Reminder"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="notes"
    )

    def __str__(self):
        return self.title