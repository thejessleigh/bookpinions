import uuid

from django.db import models
from django.utils import timezone


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    goodreads_user_id = models.IntegerField()
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, null=True)
    visibility = models.BooleanField(db_index=True)
    access_token = models.CharField(max_length=255)
    access_secret = models.CharField(max_length=255)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    indexes = [
        models.Index(
            fields=["goodreads_user_id", "visibility"], name="idx_gid_visibility"
        )
    ]

    def __str__(self):
        return "{}:{}".format(self.goodreads_user_id, self.name)
