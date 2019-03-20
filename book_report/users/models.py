from django.db import models
from django.utils import timezone


class User(models.Model):
    goodreads_user_id = models.IntegerField()
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, null=True)
    visibility = models.BooleanField()
    access_token = models.CharField(max_length=255)
    access_secret = models.CharField(max_length=255)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}:{}".format(self.goodreads_user_id, self.username)
